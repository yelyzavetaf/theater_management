from odoo import _, api, models, fields
from odoo.exceptions import ValidationError


class TheaterShowOrchestra(models.Model):
    _name = 'theater.show.orchestra'
    _description = 'Orchestra Assignment'

    event_ids = fields.Many2many(
        comodel_name='event.event',
        relation='event_show_orchestra_rel',
        column1='orc_id',
        column2='event_id',
        string="Show/Event"
    )

    instrument_id = fields.Many2one(
        comodel_name='theater.musical.instrument',
        string="Instrument",
        required=True)

    # Filter musicians who play chosen instrument
    musician_id = fields.Many2one(
        'theater.musician',
        string="Musician",
        domain="[('instrument_id', '=', instrument_id)]",
        required=True
    )

    @api.onchange('instrument_id')
    def _onchange_instrument(self):
        self.musician_id = False

    @api.depends('event_ids', 'event_ids.date_begin', 'musician_id')
    def _compute_display_name(self):
        for record in self:
            if record.event_ids:
                event_date = record.event_ids.date_begin.strftime('%Y-%m-%d')
                name = f"{record.event_ids.name} ({event_date})"

                if record.musician_id:
                    name += f" - {record.musician_id.full_name}"

                record.display_name = name
            else:
                record.display_name = "New Assignment"

    @api.constrains('musician_id', 'event_ids')
    def _check_unique_musician_per_event(self):
        for record in self:
            for event in record.event_ids:
                duplicates = event.orchestra_ids.filtered(
                    lambda m: m.musician_id == record.musician_id
                    and m.id != record.id
                )
                if duplicates:
                    raise ValidationError(_(
                        "Musician %s is already involved in this event!"
                    ) % record.musician_id.full_name)
