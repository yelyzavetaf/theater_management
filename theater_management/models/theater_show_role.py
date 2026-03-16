from odoo import _, api, models, fields
from odoo.exceptions import ValidationError


class TheaterShowRole(models.Model):
    _name = 'theater.show.role'
    _description = 'Show Role Assignment'

    event_id = fields.Many2many(comodel_name='event.event', string="Show/Event")

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
        self.artist_id = False


    @api.depends('artist_id', 'role_name')
    def _compute_display_name(self):
        for record in self:
                name = f"{record.role_name} ({record.artist_id})"
                record.display_name = name

    @api.constrains('artist_id', 'event_id')
    def _check_unique_artist_per_event(self):
        for record in self:
            for event in record.event_id:
                # Шукаємо, чи є цей артист вже в цій події (крім поточного запису)
                duplicates = event.show_role_ids.filtered(
                    lambda r: r.artist_id == record.artist_id and r.id != record.id
                )
                if duplicates:
                    raise ValidationError(_(
                        "Artist %s is already assigned to this event!"
                    ) % record.artist_id.full_name)
