import json
from odoo import models, fields, api


class Event(models.Model):
    _name = 'event.event'
    _inherit = ['event.event', 'image.mixin']

    has_orchestra = fields.Boolean(string="With Orchestra", default=True)
    has_actors = fields.Boolean(string="With Actors", default=True)

    show_role_ids = fields.Many2many(
        comodel_name='theater.show.role',
        relation='event_show_role_rel',
        column1='event_id',
        column2='role_id',
        string="Cast"
    )

    orchestra_ids = fields.Many2many(
        comodel_name='theater.show.orchestra',
        relation='event_show_orchestra_rel',
        column1='event_id',
        column2='orc_id',
        string="Orchestra"
    )

    event_type_selection = fields.Selection([
        ('show', 'Show'),
        ('rehearsal', 'Rehearsal')
    ], string="Тип події", default='show', required=True)

    description = fields.Html(
        compute='_compute_description',
        store=True,
        readonly=False,
        render_engine='qweb'  # Для Odoo 19
    )

    def _update_cover_image(self):
        """Update JSON cover image"""
        for record in self:
            if record.image_1920:
                vals = {
                    "background-image": f"url('/web/image/event.event/{record.id}/image_1920')",
                    "resize_class": "o_record_has_cover cover_auto",
                    "opacity": "0.4"
                }
                super(Event, record).write({'cover_properties': json.dumps(vals)})

    @api.model_create_multi
    def create(self, vals_list):
        records = super(Event, self).create(vals_list)
        records._update_cover_image()
        return records

    def write(self, vals):
        res = super(Event, self).write(vals)
        if 'image_1920' in vals:
            self._update_cover_image()
        return res

    @api.onchange('event_type_selection')
    def _onchange_event_type_selection(self):
        if self.event_type_selection == 'rehearsal':
            # Remove tickets if it's a rehearsal
            self.event_ticket_ids = [(5, 0, 0)]

    @api.onchange('has_actors')
    def _onchange_has_actors(self):
        if not self.has_actors:
            self.show_role_ids = [(5, 0, 0)]

    @api.onchange('has_orchestra')
    def _onchange_has_orchestra(self):
        if not self.has_orchestra:
            self.orchestra_ids = [(5, 0, 0)]

    @api.onchange('event_type_selection', 'name')
    def _onchange_event_name_prefix(self):
        prefix = "[REH] "
        if self.event_type_selection == 'rehearsal':
            if self.name and not self.name.startswith(prefix):
                self.name = prefix + self.name
        else:
            if self.name and self.name.startswith(prefix):
                self.name = self.name.replace(prefix, "")

    @api.depends('show_role_ids', 'orchestra_ids', 'event_type_selection', 'has_actors', 'has_orchestra')
    def _compute_description(self):
        for record in self:
            # Початковий HTML блок
            label = "Rehearsal" if record.event_type_selection == 'rehearsal' else "Show"
            html = f"<section class='s_text_block pb32 pt32'><h3>{label}</h3>"

            # Adding actors
            if record.has_actors and record.show_role_ids:
                html += "<h5>Cast:</h5><ul>"
                for role in record.show_role_ids:
                    artist_name = role.artist_id.full_name
                    html += f"<li><b>{role.role_name}</b> — {artist_name}</li>"
                html += "</ul>"

            # Adding orchestra
            if record.has_orchestra and record.orchestra_ids:
                html += "<h5>Orchestra:</h5><ul>"
                for orc in record.orchestra_ids:
                    musician_name = orc.musician_id.full_name
                    html += f"<li>{orc.instrument_id.name}: {musician_name}</li>"
                html += "</ul>"

            html += "</section>"
            record.description = html
