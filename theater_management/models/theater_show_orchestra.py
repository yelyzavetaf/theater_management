from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import _, api, models, fields

from odoo.exceptions import UserError, ValidationError


class TheaterShowOrchestra(models.Model):
    _name = 'theater.show.orchestra'
    _description = 'Orchestra Assignment'

    event_id = fields.Many2many(comodel_name='event.event', string="Show")

    # Поле для вибору інструмента (щоб потім відфільтрувати музикантів)
    instrument_id = fields.Many2one(comodel_name='theater.musical.instrument', string="Instrument", required=True)

    # Вибір музиканта, що грає на цьому інструменті
    musician_id = fields.Many2one(
        'theater.musician',
        string="Musician",
        domain="[('instrument_id', '=', instrument_id)]",
        required=True
    )

    @api.onchange('instrument_id')
    def _onchange_instrument(self):
        self.musician_id = False

    @api.depends('event_id', 'event_id.date_begin', 'musician_id')
    def _compute_display_name(self):
        for record in self:
            if record.event_ids:
                # Форматуємо дату (наприклад: 2024-05-20)
                event_date = record.event_id.date_begin.strftime('%Y-%m-%d')
                name = f"{record.event_id.name} ({event_date})"

                # Додамо ім'я музиканта для повноти картини, якщо він обраний
                if record.musician_id:
                    name += f" - {record.musician_id.full_name}"

                record.display_name = name
            else:
                record.display_name = "New Assignment"
