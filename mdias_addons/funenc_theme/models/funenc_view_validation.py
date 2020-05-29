# -*- coding: utf-8 -*-

from odoo.tools.convert import xml_import
from odoo import tools
from odoo.tools import view_validation
from odoo.tools.view_validation import validate
from lxml import etree

import os, logging

_logger = logging.getLogger(__name__)

def _tag_menuitem(self, rec, data_node=None, mode=None):
    '''
    改写解析xml的方法，读取其中的icon值
    :param self:
    :param rec:
    :param data_node:
    :param mode:
    :return:
    '''
    rec_id = rec.get("id")
    self._test_xml_id(rec_id)
    if rec.get('parent'):
        menu_parent_id = self.id_get(rec.get('parent',''))
    else:
        menu_parent_id = False
    values = {'parent_id': menu_parent_id}
    if rec.get('name'):
        values['name'] = rec.get('name')
    try:
        res = [self.id_get(rec.get('id', ''))]
    except:
        res = None

    if rec.get('action'):
        a_action = rec.get('action')
        action_type, action_id = self.model_id_get(a_action)
        action_type = action_type.split('.')[-1] # keep only type part
        values['action'] = "ir.actions.%s,%d" % (action_type, action_id)

        if not values.get('name') and action_type in ('act_window', 'wizard', 'url', 'client', 'server'):
            a_table = 'ir_act_%s' % action_type.replace('act_', '')
            self.cr.execute('select name from "%s" where id=%%s' % a_table, (int(action_id),))
            resw = self.cr.fetchone()
            if resw:
                values['name'] = resw[0]
    if not values.get('name'):
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
    # 读取是否有icon
    if rec.get('icon'):
        values['icon'] = rec.get('icon')
    pid = self.env['ir.model.data']._update('ir.ui.menu', self.module, values, rec_id, noupdate=self.isnoupdate(data_node), mode=self.mode, res_id=res and res[0] or False)
    if rec_id and pid:
        self.idref[rec_id] = int(pid)
    return 'ir.ui.menu', pid


def relaxng(view_type):
    """ Return a validator for the given view type, or None. """
    cur_path, _ = os.path.split(os.path.realpath(__file__))
    if view_type not in view_validation._relaxng_cache:
        with tools.file_open(os.path.join(cur_path, '..', 'rng', '%s_view.rng' % view_type)) as frng:
            try:
                relaxng_doc = etree.parse(frng)
                view_validation._relaxng_cache[view_type] = etree.RelaxNG(relaxng_doc)
            except Exception as e:
                _logger.exception('Failed to load RelaxNG XML schema for views validation')
                view_validation._relaxng_cache[view_type] = None
    return view_validation._relaxng_cache[view_type]


xml_import._tag_menuitem = _tag_menuitem
view_validation.relaxng = relaxng

for index, pred in enumerate(view_validation._validators['tree']):
    if pred.__name__ == 'valid_field_in_tree':
        view_validation._validators['tree'].pop(index)
        break

@validate('tree')
def valid_field_in_tree(arch):
    """ Children of ``tree`` view must be ``field`` or ``button``."""
    # return all(
    #     child.tag in ('field', 'button', 'widget')
    #     for child in arch.xpath('/tree/*')
    # )
    return True