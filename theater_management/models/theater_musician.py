from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import _, api, models, fields


class TheaterMusician(models.Model):

    _name = 'theater.musician'
    _description = 'Musician'
    _inherit = 'theater.abstract.person'
    _rec_names_search = 'full_name'

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='System User',
        ondelete='restrict',
    )

    instrument_id = fields.Many2one(
        comodel_name='theater.musical.instrument',
        string='Musical instrument',
    )

    joined_date = fields.Date(required=True)

    experience = fields.Integer(
        compute='_compute_experience',
        string="Years of experience",
        readonly=True,
    )

    orchestra_ids = fields.One2many(
        comodel_name='theater.show.orchestra',
        inverse_name='musician_id',
    )

    @api.depends('full_name')
    def _compute_display_name(self):
        """
        Format the musician's display name to include their musical instrument.
        Example: "Ivanov Ivan (Violin)"
        """
        for musician in self:
            musician.display_name = (
                f"{musician.full_name} ({musician.instrument_id.name})"
            )

    @api.depends('experience')
    def _compute_experience(self):
        """
        Calculate years of professional experience based on joined date.
        """
        for musician in self:
            today = date.today()
            diff = relativedelta(today, musician.joined_date)
            musician.experience = diff.years

    def get_participation_data(self, date_from=False, date_to=False):
        """Метод для збору подій та годин для PDF"""
        self.ensure_one()
        # Шукаємо всі записи в оркестрі для цього музиканта
        domain = [('musician_id', '=', self.id)]
        if date_from:
            domain.append(('event_ids.date_begin', '>=', date_from))
        if date_to:
            domain.append(('event_ids.date_begin', '<=', date_to))

        orchestra_lines = self.env['theater.show.orchestra'].search(domain)
        events = orchestra_lines.mapped('event_ids')

        report_lines = []
        total_hours = 0.0
        for event in events:
            hours = (event.date_end - event.date_begin).total_seconds() / 3600
            total_hours += hours
            report_lines.append({
                'name': event.name,
                'date': event.date_begin,
                'hours': round(hours, 2)
            })
        return {'events': report_lines, 'total': round(total_hours, 2)}

