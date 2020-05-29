# -*- coding: utf-8 -*-
{
    'name': "maintenance_management",
    'summary': """funenc auto gen project""",
    'description': """
       Long description of module's purpose
    """,

    'author': "crax",
    'website': "http://www.funenc.com",

    'category': 'funenc',
    'version': '1.0',

    'depends': ['base', 'bus', 'metro_park_base'],

    'data': [
        'security/ir.model.access.csv',
        'security/group_data.xml',
        'views/views.xml',
        'views/assets.xml',
        'views/maintenance/server_client.xml',
        'views/maintenance/call_record.xml',
        'views/maintenance/diagnosis_record.xml',
        'views/maintenance/configuration_information.xml',
        'views/timing_task.xml',
        'views/maintenance/switch_log.xml',
        'views/configuration_file.xml',
        'views/maintenance/page_operation_record.xml',
    ],

    'qweb': [
        'static/xml/*.xml',
    ],
    'application': True
}
