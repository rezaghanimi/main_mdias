# -*- coding: utf-8 -*-
{
    'name': "metro_park_base",
    'summary': """车辆段基础数据""",
    'description': """
        车辆段自动化基础数据
    """,

    'author': "funenc",
    'website': "http://www.funenc.com",

    'category': 'funenc',
    'version': '1.0',

    'depends': ['base',
                'funenc_wechat',
                'odoo_groups_manage',
                'base_session_store_psql',
                'odoo_operation_log',
                'funenc_socket_io'],

    'data': [
        'security/sys_group_data.xml',
        'security/ir.model.access.csv',
        "data/selections.xml",
        'security/security.xml',
        'views/login_extend.xml',
        'views/assets.xml',
        "views/root_menu.xml",
        "views/line.xml",
        "views/major.xml",
        "views/dev_type.xml",
        "views/location_type.xml",
        "views/major_type.xml",
        "views/location.xml",
        "views/rails_sec.xml",
        "views/rail_type.xml",
        "views/rail_state.xml",
        "views/park_map.xml",
        "views/change_password_wizard.xml",
        "views/group_ext.xml",
        "views/electric_area.xml",
        "views/user_manage.xml",
        "views/system_config.xml",
        "views/dev_standard.xml",
        "views/user_preference_extend.xml",
        "views/dev_unit.xml",
        "views/base_app_search.xml",
        "views/signals.xml",
        "views/switches.xml",

        "views/time_table.xml",
        "views/time_table_data.xml",
        'views/time_table_syn_log.xml',

        'views/rail_property.xml',
        'views/other_interlock.xml',
        'views/backup_electric_area_info.xml',
        'views/btn_table.xml',
        'views/funenc_login.xml',
        'views/code_table.xml',
        'views/ats_address.xml',
        'views/selections.xml',
        "views/common_log.xml",

        "data/cron_to_login_clear.xml",
        "data/dev_type.xml",
        "data/location_type.xml",
        "data/rail_type.xml",
        "data/rail_state.xml",
        "data/rail_property.xml",
        "data/dev_standard.xml",
        "data/major.xml",
        "data/major_type.xml",
        "data/department_property.xml",
        "data/other_interlock.xml",
        "data/sequence_number.xml",
        "data/park_area.xml",
        'views/busy_board.xml'
    ],

    'qweb': [
        'static/xml/funenc_side_menu.xml',
        'static/xml/misc.xml'
    ],

    'application': True
}
