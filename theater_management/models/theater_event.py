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



