import datetime
from dateutil.relativedelta import relativedelta
from odoo.tests.common import TransactionCase


class TestTheaterManagementCommon(TransactionCase):

    def setUp(self):
        super(TestTheaterManagementCommon, self).setUp()
        self.artist = self.env['theater.artist'].create({
            'first_name': 'Taras',
            'last_name': 'Shevchenko',
            'phone_number': '0671234567',
            'birth_date': datetime.date.today() - relativedelta(years=30),
            'joined_date': datetime.date.today() - relativedelta(years=5),
            'performer_type': 'actor',
        })

        self.artist2 = self.env['theater.artist'].create({
            'first_name': 'Benedict',
            'last_name': 'Cumberbatch',
            'phone_number': '0671112233',
            'birth_date': '1976-07-19',
            'joined_date': '2020-01-01',
            'performer_type': 'actor',
        })

        self.guitar = self.env['theater.musical.instrument'].create({
            'name': 'Guitar',
            'category': 'strings',
        })

        self.piano = self.env['theater.musical.instrument'].create({
            'name': 'Piano',
            'category': 'keyboard',
        })

        self.musician = self.env['theater.musician'].create({
            'first_name': 'Jimi',
            'last_name': 'Hendrix',
            'phone_number': '0671112233',
            'birth_date': datetime.date(1942, 11, 27),
            'joined_date': datetime.date.today() - relativedelta(years=3),
            'instrument_id': self.guitar.id,
        })

        self.event = self.env['event.event'].create({
            'name': 'Rock Concert',
            'date_begin': datetime.datetime(2026, 5, 20, 19, 0, 0),
            'date_end': datetime.datetime(2026, 5, 20, 21, 0, 0),
        })

        self.event2 = self.env['event.event'].create({
            'name': 'Old sea',
            'date_begin': datetime.datetime(2026, 6, 1, 19, 0, 0),
            'date_end': datetime.datetime(2026, 6, 1, 22, 0, 0),
        })
