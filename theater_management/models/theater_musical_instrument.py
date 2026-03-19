from odoo import _, api, models, fields


class TheaterMusicalInstrument(models.Model):
    """
    Represent a musical instrument used in the theater's orchestra.

    This model categorizes instruments (e.g., strings, percussion) and
    maintains a relationship with the musicians who play them. It also
    tracks the total count of associated musicians for statistical purposes.
    """
    _name = 'theater.musical.instrument'
    _description = 'Musical Instrument'
    _order = 'name'

    name = fields.Char(
        string="Instrument Name",
        required=True,
        translate=True
    )
    category = fields.Selection([
        ('strings', 'Strings'),
        ('woodwinds', 'Woodwinds'),
        ('brass', 'Brass'),
        ('percussion', 'Percussion'),
        ('keyboard', 'Keyboard')
    ], required=True, translate=True)

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
        """
        Calculate the total number of musicians assigned to this instrument.

        Triggered whenever the 'musician_ids' list changes. The result is
        stored in the database to allow fast filtering and grouping.
        """
        for record in self:
            record.number_of_musicians = len(record.musician_ids)
