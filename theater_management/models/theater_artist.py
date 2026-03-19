from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, models, fields


class TheaterArtist(models.Model):
    """
    Represent a performing artist within the theater management system.

    This model extends 'theater.abstract.person' to include specific attributes
    for stage performers, such as their specialization (acting, dancing,
    singing), dance styles, and historical role assignments. It automatically
    calculates experience based on the joined date.
    """
    _name = 'theater.artist'
    _description = 'Artist'
    _inherit = 'theater.abstract.person'
    _rec_names_search = 'full_name'

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='System User',
        ondelete='restrict',
    )

    performer_type = fields.Selection([
        ('actor', 'Actor/Actress'),
        ('dancer', 'Dancer'),
        ('soloist', 'Solo Singer'),
        ('chorister', 'Choir Member'),
        ('extra', 'Extra (Mass Scene)')
    ], required=True, help="Select the primary role of the artist")

    dance_style = fields.Selection([
        ('ballet', 'Ballet'),
        ('modern', 'Modern'),
        ('folk', 'Folk')
    ], help="Only for dancers")

    role_ids = fields.One2many(
        comodel_name='theater.show.role',
        inverse_name='artist_id',
        string='Roles',
    )

    joined_date = fields.Date(required=True)

    experience = fields.Integer(
        compute='_compute_experience',
        string="Years of experience",
        readonly=True,
    )

    @api.depends('full_name')
    def _compute_display_name(self):
        """
        Format the musician's display name to include their musical instrument.
        Example: "Ivanov Ivan (Violin)"
        """
        for artist in self:
            artist.display_name = (
                f"{artist.full_name} ({artist.performer_type})"
            )

    @api.depends('experience')
    def _compute_experience(self):
        """
        Calculate years of professional experience based on joined date.
        """
        for artist in self:
            today = date.today()
            diff = relativedelta(today, artist.joined_date)
            artist.experience = diff.years
