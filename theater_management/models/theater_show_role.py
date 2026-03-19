from odoo import _, api, models, fields
from odoo.exceptions import ValidationError


class TheaterShowRole(models.Model):
    """
    Manage the assignment of specific artistic roles to performers
    for theater events.

    This model links artists to events based on their performance category
    (acting,dancing, singing) and ensures that each assignment is unique
    per event to prevent scheduling or casting conflicts.
    """
    _name = 'theater.show.role'
    _description = 'Show Role Assignment'

    event_ids = fields.Many2many(
        comodel_name='event.event',
        relation='event_show_role_rel',
        column1='role_id',
        column2='event_id',
        string="Show/Event"
    )

    role_name = fields.Char(string="Specific Role", required=True)
    performer_type = fields.Selection([
        ('actor', 'Actor/Actress'),
        ('dancer', 'Dancer'),
        ('soloist', 'Solo Singer'),
        ('chorister', 'Choir Member'),
        ('extra', 'Extra (Mass Scene)')
    ], required=True, string="Role Category")

    artist_id = fields.Many2one(
        comodel_name='theater.artist',
        string="Artist",
        domain="[('performer_type', '=', performer_type)]",
        required=True,
    )

    description = fields.Char()

    # Clearing artist_id if performer_type has changed
    @api.onchange('performer_type')
    def _onchange_performer_type(self):
        """Reset the selected artist if the role category
        changes to ensure compatibility."""
        self.artist_id = False

    @api.depends('artist_id', 'role_name')
    def _compute_display_name(self):
        """
        Construct a readable name for the role assignment.

        Combines the character name and the artist's name to provide clear
        identification within the system's relational fields.
        """
        for record in self:
            name = f"{record.role_name} ({record.artist_id})"
            record.display_name = name

    @api.constrains('artist_id', 'event_ids')
    def _check_unique_artist_per_event(self):
        """
        Validate that artist isn't assigned to same event more than once.

        Iterates through linked events to check for existing assignments for
        the same artist, raising a ValidationError if a duplicate is found.
        """
        for record in self:
            for event in record.event_ids:
                duplicates = event.show_role_ids.filtered(
                    lambda r: r.artist_id == record.artist_id
                    and r.id != record.id
                )
                if duplicates:
                    raise ValidationError(_(
                        "Artist %s is already assigned to this event!"
                    ) % record.artist_id.full_name)
