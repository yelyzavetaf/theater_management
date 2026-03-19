from .common import TestTheaterManagementCommon


class TestTheaterMusicalInstrument(TestTheaterManagementCommon):

    def test_01_instrument_creation(self):
        """Check if Guitar is created correctly with default values."""
        self.guitar = self.env['theater.musical.instrument'].create({
            'name': 'Guitar2',
            'category': 'strings',
        })

        self.assertEqual(self.guitar.name, 'Guitar2')
        self.assertEqual(self.guitar.category, 'strings')
        self.assertTrue(self.guitar.active,
                        "Instrument should be active by default")
        self.assertEqual(self.guitar.number_of_musicians, 0,
                         "Initial count should be 0")
