{
    'name': 'Theater management',
    'version': "19.0.1.0.0",
    "author": "Lisa",
    "website": "https://www.lipsum.com/",
    'category': 'Extra Tools',
    'summary': 'Allows to track shows and actors',
    "license": "OPL-1",
    'depends': ['base', 'event'],

    'data': [
        # "security/hr_hospital_groups.xml",
        "security/ir.model.access.csv",
        # "security/hr_hospital_security.xml",
        "data/theater_musical_instruments.xml",
        "views/theater_menus.xml",
    ],

    'images': ['static/description/banner.png', 'static/description/icon.png'],
}
