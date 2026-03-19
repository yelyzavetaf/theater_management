from datetime import date
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError
from .common import TestTheaterManagementCommon


class TestTheaterArtist(TestTheaterManagementCommon):

    def test_01_compute_experience(self):
        """Check automatical experience calculation."""
        self.assertEqual(
            self.artist.experience, 5,
            "Experience should be 5 years, as joined_date was 5 years ago."
        )

        self.artist.joined_date = date.today() - relativedelta(years=10)
        self.artist._compute_experience()
        self.assertEqual(self.artist.experience, 10,
                         msg="Experience should be updated to 10 years.")

    def test_02_phone_validation(self):
        with self.assertRaises(ValidationError,
                               msg="Should raise short number error"):
            self.artist.write({'phone_number': '123'})

        with self.assertRaises(ValidationError,
                               msg="Should contain numbers only"):
            self.artist.write({'phone_number': '067abc4567'})

        self.artist.write({'phone_number': '0990001122'})
        self.assertEqual(self.artist.phone_number, '0990001122')
