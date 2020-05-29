# -*- coding: utf-8 -*-
{
    'name': "project_manage",
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
        'security/group_data.xml',
        'security/ir.model.access.csv',
        "views/root_menu.xml",
        "views/project_manage.xml",
        "views/report_content.xml",
        "views/project_type.xml"
    ],

    'qweb': [
        "static/xml/misc.xml"
    ],

    'application': True
}