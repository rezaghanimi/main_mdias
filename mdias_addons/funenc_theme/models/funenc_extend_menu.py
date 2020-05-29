# -*- coding: utf-8 -*-

from odoo.tools.convert import xml_import

'''
继承ir.ui.menu创建图标字段，并返回图标字段信息
'''

import operator

from odoo import api, fields, models, tools


class FunencExtendMenu(models.Model):
    '''
    扩展，添加font_icon，用于前端显示字体图标
    '''
    _inherit = 'ir.ui.menu'

    font_icon = fields.Char(string='font icon')

    @api.model
    @tools.ormcache_context('self._uid', 'debug', keys=('lang',))
    def load_menus(self, debug):
        """ Loads all menu items (all applications and their sub-menus).

        :return: the menu root
        :rtype: dict('children': menu_nodes)
        """
        fields = ['name', 'sequence', 'parent_id', 'action', 'web_icon', 'font_icon', 'web_icon_data']
        menu_roots = self.get_user_roots()
        menu_roots_data = menu_roots.read(fields) if menu_roots else []
        menu_root = {
            'id': False,
            'name': 'root',
            'parent_id': [-1, ''],
            'children': menu_roots_data,
            'all_menu_ids': menu_roots.ids,
        }

        if not menu_roots_data:
            return menu_root

        # menus are loaded fully unlike a regular tree view, cause there are a
        # limited number of items (752 when all 6.1 addons are installed)
        menus = self.search([('id', 'child_of', menu_roots.ids)])
        menu_items = menus.read(fields)

        # add roots at the end of the sequence, so that they will overwrite
        # equivalent menu items from full menu read when put into id:item
        # mapping, resulting in children being correctly set on the roots.
        menu_items.extend(menu_roots_data)
        menu_root['all_menu_ids'] = menus.ids  # includes menu_roots!

        # make a tree using parent_id
        menu_items_map = {menu_item["id"]: menu_item for menu_item in menu_items}
        for menu_item in menu_items:
            parent = menu_item['parent_id'] and menu_item['parent_id'][0]
            if parent in menu_items_map:
                menu_items_map[parent].setdefault(
                    'children', []).append(menu_item)

        # sort by sequence a tree using parent_id
        for menu_item in menu_items:
            menu_item.setdefault('children', []).sort(key=operator.itemgetter('sequence'))

        (menu_roots + menus)._set_menuitems_xmlids(menu_root)

        return menu_root

def _tag_menuitem(self, rec, data_node=None, mode=None):
    rec_id = rec.get("id")
    self._test_xml_id(rec_id)

    # The parent attribute was specified, if non-empty determine its ID, otherwise
    # explicitly make a top-level menu
    if rec.get('parent'):
        menu_parent_id = self.id_get(rec.get('parent',''))
    else:
        # we get here with <menuitem parent="">, explicit clear of parent, or
        # if no parent attribute at all but menu name is not a menu path
        menu_parent_id = False
    values = {'parent_id': menu_parent_id}
    if rec.get('name'):
        values['name'] = rec.get('name')
    try:
        res = [ self.id_get(rec.get('id','')) ]
    except:
        res = None

    if rec.get('action'):
        a_action = rec.get('action')

        # determine the type of action
        action_model, action_id = self.model_id_get(a_action)
        action_type = action_model.split('.')[-1] # keep only type part
        values['action'] = "ir.actions.%s,%d" % (action_type, action_id)

        if not values.get('name') and action_type in ('act_window', 'wizard', 'url', 'client', 'server'):
            resw = self.env[action_model].sudo().browse(action_id).name
            if resw:
                values['name'] = resw

    if not values.get('name'):
        # ensure menu has a name
        values['name'] = rec_id or '?'

    if rec.get('sequence'):
        values['sequence'] = int(rec.get('sequence'))

    values['active'] = self.nodeattr2bool(rec, 'active', default=True)

    if rec.get('groups'):
        g_names = rec.get('groups','').split(',')
        groups_value = []
        for group in g_names:
            if group.startswith('-'):
                group_id = self.id_get(group[1:])
                groups_value.append((3, group_id))
            else:
                group_id = self.id_get(group)
                groups_value.append((4, group_id))
        values['groups_id'] = groups_value

    if not values.get('parent_id'):
        if rec.get('web_icon'):
            values['web_icon'] = rec.get('web_icon')

    # read font icon
    if rec.get('font_icon'):
        values['font_icon'] = rec.get('font_icon')

    xid = self.make_xml_id(rec_id)
    data = dict(xml_id=xid, values=values, noupdate=self.isnoupdate(data_node))
    self.env['ir.ui.menu']._load_records([data], self.mode == 'update')

xml_import._tag_menuitem = _tag_menuitem
