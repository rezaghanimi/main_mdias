# -*- coding: utf-8 -*-
{
    'name': "metro_park_production",

    'summary': """
        生产信息管理模块""",

    'description': """
        Long description of module's purpose
    """,

    'author': "funenc",
    'website': "http://www.funenc.com",

    "category": "funenc",
    'version': '0.1',

    'depends': ['base',
                'metro_park_base',
                'metro_park_dispatch',
                'funenc_theme',
                'metro_park_interlock',
                'metro_park_maintenance',
                'maintenance_management',
                'odoo_operation_log'],

    'data': [
        'security/ir.model.access.csv',
        'data/group_data.xml',

        'views/other/assets.xml',
        'views/other/big_screen.xml',
        'views/handover_work/parker_handover.xml',
        'views/handover_work/wizard/handover_authentication.xml',
        'views/handover_work/dispatcher_handover.xml',
        'views/handover_work/checker_handover.xml',
        'views/handover_work/signaler_handover.xml',
        'views/other/metro_park_production_files_view.xml',
        'views/other/rule_info.xml',
        'views/other/video.xml',
        'views/other/early_waring_train_config.xml',
        'views/other/statistics_report.xml',
        'views/template/early_waring_message.xml',
        'views/other/video_config.xml',
        'views/other/ir_cron.xml',
        'views/menus.xml',

        'data/base_group.xml',
        'data/early_waring_data.xml',
        'data/file_type.xml',

    ],

    'qweb': [
        "static/xml/search.xml",
        "static/xml/construction_plan_search.xml",
        "static/xml/handover_search.xml",
        "static/xml/handover_tree_button.xml",
        "static/xml/templates.xml",
        "static/xml/report_client.xml"
    ],
    'application': True

}
