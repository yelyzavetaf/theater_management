from odoo import _, api, models, fields
from odoo.exceptions import ValidationError


class TheaterShowOrchestra(models.Model):
    """
    Manage the assignment of musicians and their instruments to events.

    This model acts as a bridge between events and the orchestra members,
    ensuring that each musician is assigned based on their specific instrument
    and preventing double-booking of the same artist for a single event.
    """
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
        required=True)

    # Filter musicians who play chosen instrument
    musician_id = fields.Many2one(
        comodel_name='theater.musician',
        domain="[('instrument_id', '=', instrument_id)]",
        required=True
    )

    @api.onchange('instrument_id')
    def _onchange_instrument(self):
        """Reset the selected musician if chosen instrument category changes"""
        self.musician_id = False

    @api.depends('event_ids', 'event_ids.date_begin', 'musician_id')
    def _compute_display_name(self):
        """
        Dynamic generation of the record's name.

        Combines the event name, its start date, and the musician's full name
        to provide a clear identification in breadcrumbs and relational fields.
        """
        for record in self:
            if record.event_ids:
                name = f"{record.event_ids[0].name}"

                if record.musician_id:
                    name += f" - {record.musician_id.full_name}"

                record.display_name = name
            else:
                record.display_name = "New Assignment"

    @api.constrains('musician_id', 'event_ids')
    def _check_unique_musician_per_event(self):
        """
        Validate that a musician is not added multiple times to the same event.

        Prevents data duplication and scheduling errors by checking existing
        orchestra assignments linked to the same event.
        """
        for record in self:
            for event in record.event_ids:
                duplicates = event.orchestra_ids.filtered(
                    lambda m, rec=record: m.musician_id == rec.musician_id
                    and m.id != rec.id
                )
                if duplicates:
                    raise ValidationError(_(
                        "Musician %s is already involved in this event!",
                        record.musician_id.full_name
                    ))
