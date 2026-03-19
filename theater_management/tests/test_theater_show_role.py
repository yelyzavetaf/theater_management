from odoo.exceptions import ValidationError

from .common import TestTheaterManagementCommon


class TestTheaterShowRole(TestTheaterManagementCommon):

    def test_01_unique_artist_constraint(self):
        """Check artist not to have two roles in the same show."""
        self.env['theater.show.role'].create({
            'role_name': 'Sailor',
            'performer_type': 'actor',
            'artist_id': self.artist.id,
            'event_ids': [(4, self.event.id)],
        })

        with self.assertRaises(ValidationError, msg="Should raise ValidationError for duplicate artist in the same event"):
            self.env['theater.show.role'].create({
                'role_name': 'Ghost',
                'performer_type': 'actor',
                'artist_id': self.artist.id,
                'event_ids': [(4, self.event.id)],
            })
