# -*- coding: utf-8 -*-
{
    'name': "mdias_test",
    'summary': """funenc auto gen project""",
    'description': """
        funenc auto gen project
    """,

    'author': "crax",
    'website': "http://www.funenc.com",

    'category': 'funenc',
    'version': '1.0',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        "views/root_menu.xml",
        'views/test_message_template.xml',
        "views/mdias_test.xml",
        "views/test_client.xml",
        "views/assets.xml"
    ],

    'qweb': [
    ],
    'application': True
}