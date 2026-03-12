from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import _, api, models, fields
from odoo.exceptions import ValidationError


class TheaterMusicalInstrument(models.Model):
    _name = 'theater.musical_instrument'
    _description = 'Musical Instrument'
    _order = 'name'

    name = fields.Char(string="Instrument Name", required=True)
    category = fields.Selection([
        ('strings', 'Strings'),    # Струнні
        ('woodwinds', 'Woodwinds'), # Духові дерев'яні
        ('brass', 'Brass'),        # Духові мідні
        ('percussion', 'Percussion'), # Ударні
        ('keyboard', 'Keyboard')   # Клавішні
    ], required=True)

    musician_ids = fields.One2many(
        comodel_name='theater.musician',
        inverse_name='instrument_id',
        string='Musicians',
    )

    active = fields.Boolean(default=True)
