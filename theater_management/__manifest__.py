{
    'name': 'Theater management',
    'version': "19.0.1.0.0",
    "author": "Lisa",
    "website": "https://www.lipsum.com/",
    'category': 'Extra Tools',
    'summary': 'Allows to track shows and actors',
    "license": "OPL-1",
    'depends': ['base', 'event', 'website_event', 'website'],

    'data': [
        # "security/hr_hospital_groups.xml",
        "security/ir.model.access.csv",
        # "security/hr_hospital_security.xml",
        "data/theater_musical_instrument_data.xml",

        "views/theater_menus.xml",
        "views/theater_musical_instrument_views.xml",
        "views/theater_musician_views.xml",
        "views/theater_artist_views.xml",
        "views/theater_show_role_views.xml",
        "views/theater_show_orchestra_views.xml",
        "views/theater_event_views.xml",

    ],
    'demo': [
        "demo/theater_musician_demo.xml",
        "demo/theater_artist_demo.xml",
    ],

    'images': ['static/description/banner.png', 'static/description/icon.png'],
}
