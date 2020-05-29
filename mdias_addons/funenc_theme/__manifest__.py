# -*- coding: utf-8 -*-
{
    'name': "funenc_theme",

    'summary': """
        北京富能通科技有限公司基础框架""",

    'description': """
        北京富能通科技有限公司基础框架
    """,

    'author': "chun.xu@funenc.com",
    'website': "http://www.funenc.com",

    'category': 'funenc',
    'version': '2.0.1',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/base.xml',
        'views/views.xml',
        'views/uninstall.xml',
        'views/funenc_login.xml',
        'views/theme_style.xml',
        'views/menus.xml',

    ],

    'qweb': [
        'static/xml/funenc_selection.xml',
        'static/xml/funenc_side_menu.xml',
        'static/xml/funenc_user_menu.xml',
        'static/xml/funenc_table.xml',
        'static/xml/funenc_many2one.xml',
        'static/xml/funenc_datetime_picker.xml',
        'static/xml/funenc_left_tree_list.xml',
        'static/xml/funenc_theme_color.xml',
        'static/xml/funenc_search.xml',
        'static/xml/funenc_tab_page.xml',
        'static/xml/funenc_expand_widget.xml',
        'static/xml/funenc_controller.xml',
        'static/xml/funenc_system_style.xml'
        'static/xml/funenc_theme_style.xml',
        'static/xml/list_tab_template.xml',
        'static/xml/include_template.xml',
        'static/xml/fields.xml',
        'static/xml/misc.xml'
    ],
    "application": True
}
