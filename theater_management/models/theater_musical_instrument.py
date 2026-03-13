from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import _, api, models, fields
from odoo.exceptions import ValidationError


class TheaterMusicalInstrument(models.Model):
    _name = 'theater.musical.instrument'
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

    active = fields.Boolean(default=True)

    musician_ids = fields.One2many(
        comodel_name='theater.musician',
        inverse_name='instrument_id',
        string='Musicians',
    )

    number_of_musicians = fields.Integer(
        string='Number of Musicians',
        compute='_compute_number_of_musicians',
        store=True
    )

    @api.depends('musician_ids')
    def _compute_number_of_musicians(self):
        for record in self:
            record.number_of_musicians = len(record.musician_ids)

