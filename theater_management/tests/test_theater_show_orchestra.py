from .common import TestTheaterManagementCommon


class TestTheaterShowOrchestra(TestTheaterManagementCommon):

    def test_01_onchange_instrument(self):
        """Check if musician field gets empty after instrument change."""
        assignment = self.env['theater.show.orchestra'].new({
            'instrument_id': self.guitar.id,
            'musician_id': self.musician.id,
        })
        assignment._onchange_instrument()
        assignment.instrument_id = self.piano
        assignment._onchange_instrument()
        self.assertFalse(assignment.musician_id, "Musician should be reset when instrument changes.")
