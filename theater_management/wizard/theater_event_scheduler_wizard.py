from odoo import _, fields, models
from odoo.exceptions import ValidationError


class EventSchedulerWizard(models.TransientModel):
    _name = 'theater.event.scheduler.wizard'
    _description = 'Schedule Event'

    event_id = fields.Many2one(comodel_name='event.event', string="Event", required=True)

    schedule_line_ids = fields.One2many(
        comodel_name='theater.event.scheduler.line',
        inverse_name='wizard_id',
        string="Schedules"
    )

    def action_schedule(self):
        self.ensure_one()
        source = self.event_id
        duration = source.date_end - source.date_begin
        new_events_list = []

        for line in self.schedule_line_ids:
            start = line.date
            end = line.date + duration

            conflicts = self.env['event.event'].search([
                            ('address_id', '=', source.address_id.id),
                            ('date_begin', '<', end),
                            ('date_end', '>', start),
                        ])

            if conflicts:
                raise ValidationError(_(
                    "Time slot conflict for %s! Time reserved for event: %s"
                ) % (start.strftime('%d.%m %H:%M'), conflicts[0].name))

            vals = source.copy_data()[0]

            vals.update({
                'name': source.name,
                'date_begin': line.date,
                'date_end': line.date + duration,
                'show_role_ids': [(6, 0, source.show_role_ids.ids)],
                'orchestra_ids': [(6, 0, source.orchestra_ids.ids)],
            })

            new_event = self.env['event.event'].create(vals)
            new_events_list.append(new_event.id)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'event.event',
            'view_mode': 'list,form',
            'domain': [('id', 'in', new_events_list)],
            'name': 'Scheduled Events',
        }


class EventSchedulerLine(models.TransientModel):
    _name = 'theater.event.scheduler.line'
    _description = 'Schedule Line'

    wizard_id = fields.Many2one(comodel_name='theater.event.scheduler.wizard', ondelete='cascade')
    date = fields.Datetime(string="Date", required=True)
