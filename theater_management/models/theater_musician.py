from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import _, api, models, fields

from odoo.exceptions import UserError, ValidationError


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
