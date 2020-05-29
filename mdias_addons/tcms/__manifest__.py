# -*- coding: utf-8 -*-
{
    'name': "tcms",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'maintenance_management'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/break_info.xml',
        'views/equipment_energy.xml',
        'views/eb_info.xml',
        'views/compressor_work_time_l.xml',
        'views/compressor_work_time_2.xml',
        'views/renewable_electricity_l.xml',
        'views/pressure_switch.xml',
        'views/stop_brake_side_switch.xml',
        'views/stop_no_ease_side_switch.xml',
        'views/train_close_side_switch.xml',
        'views/train_complete_side_switch.xml',
        'views/battery_bus_voltage_switch.xml',
        'views/battery_bus_current_switch.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
