from odoo import api, models, fields


class TheaterShowRole(models.Model):
    _name = 'theater.show.role'
    _description = 'Show Role Assignment'

    event_id = fields.Many2one(comodel_name='event.event', string="Show/Event", ondelete='cascade')

    role_name = fields.Char(string="Specific Role", placeholder="e.g. Hamlet, Lead Dancer")
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
        domain="[('performer_type', '=', performer_type)]")

    description = fields.Char()

    # Clearing artist_id if performer_type has changed
    @api.onchange('performer_type')
    def _onchange_performer_type(self):
        self.artist_id = False