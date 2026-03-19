from .common import TestTheaterManagementCommon


class TestTheaterMusician(TestTheaterManagementCommon):

    def test_01_musician_display_name(self):
        self.musician._compute_display_name()
        expected_name = "Hendrix Jimi (Guitar)"
        self.assertEqual(self.musician.display_name, expected_name,
                         "Display name should include the instrument name.")

    def test_02_instrument_relation(self):
        self.assertEqual(self.guitar.number_of_musicians, 1,
                         "The instrument's musician counter should have updated.")