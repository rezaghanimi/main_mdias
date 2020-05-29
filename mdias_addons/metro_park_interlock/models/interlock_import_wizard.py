# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import xlrd
import base64
import re


class InterLockImportWizard(models.Model):
    '''
    导入联锁文件向导
    '''
    _name = 'metro_park.interlock.import_wizard'
    _description = '导入联锁文件向导'
    _track_log = True

    location = fields.Many2one(string="位置",
                               comodel_name="metro_park_base.location",
                               required=True)
    file_name = fields.Char(string='文件名称',
                            default="请选择联锁文件")
    interlock_file = fields.Binary(string='联锁文件',
                                   required=True)

    @api.model
    def get_import_interlock_table_wizard(self):
        '''
        取得导入联锁表向导
        :return:
        '''
        form_id = self.env.ref(
            'metro_park_interlock.metro_park_interlock_import_wizard_form').id

        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "metro_park.interlock.import_wizard",
            "name": "联锁表导入",
            "target": "new",
            "views": [[form_id, "form"]]
        }

    @api.model
    def get_all_switches(self, rows):
        '''
        创建缺失的道岔, 设计的时候考虑了[()]的情况
        :return:
        '''
        all_switches = self.env['metro_park_base.switches'].search([])
        return {switch['name']: switch['id'] for switch in all_switches}

    @api.multi
    def on_import_inter_lock_file(self):
        '''
        导入联锁文件
        :return:
        '''
        old = self.env['metro_park.interlock.route']\
            .search([('location', '=', self.location.id)])
        if old:
            raise exceptions.ValidationError('此位置联锁已经导入')

        # 获取execl中数据
        bin_data = base64.b64decode(self.interlock_file)
        workbook = xlrd.open_workbook(file_contents=bin_data)

        # 根据sheet索引或者名称获取sheet内容
        sheet2 = workbook.sheet_by_index(0)  # sheet索引从0开始
        rows = []
        for row in range(0, sheet2.nrows):
            rows.append(sheet2.row_values(row))

        # 前三行不要
        rows = rows[3:]

        # 先期处理数据，用于处理合并单元格
        prev_row = None
        for index, row in enumerate(rows):
            if prev_row:
                if row[0] == '' and prev_row:
                    row[0] = prev_row[0]
                if row[1] == '' and prev_row:
                    row[1] = prev_row[1]
                if row[2] == '':
                    row[2] = prev_row[2]
                if row[1] and row[1] == '由':
                    row[1] = row[2]
            prev_row = row

        # 缓存场段所有信号机
        all_signals = self.env['metro_park_base.signals'].search(
            [('location', '=', self.location.id)]
        )
        signal_cache = {signal['name']: signal['id'] for signal in all_signals}

        # 缓存场段所有道岔
        all_switches = self.env['metro_park_base.switches'].search(
            [('location', '=', self.location.id)]
        )
        switch_cache = {switch['name']: switch['id']
                        for switch in all_switches}

        # 缓存场段所有区段
        secs = self.env['metro_park_base.rails_sec'].search(
            [('location', '=', self.location.id)]
        )
        sec_cache = {sec['no']: sec['id'] for sec in secs}

        # 其它(联锁)
        other_interlocks = self.env["metro_park_base.other_interlock"]\
            .search([])
        other_interlock_cache = {
            record.name: record.id for record in other_interlocks}

        def create_signal_info(row):
            '''
            创建信号机信息
            :param row:
            :return:
            '''
            signal = row[12]
            display = row[13]
            indicator = row[14]
            record = self.env['metro_park.interlock.signal_infos'].create({
                'signal': signal_cache[signal.rstrip('DdLl').upper()],
                'display': display,
                'indicator': indicator
            })
            return record.id

        def create_switch_info(row):
            '''
            创建道岔信息
            :param row:
            :return:
            '''

            vals = []
            switches = row[15]
            switch_array = str(switches).split(',')
            for data_index, switch in enumerate(switch_array):
                switch = switch.strip()
                if switch == "":
                    continue
                val = {
                    'index': data_index,
                    'location': self.location.id,
                    'is_reverse': False,
                    'is_protect': False
                }

                # 防护加反位
                sub_switch_infos = []
                if switch.startswith('[('):
                    val.update({
                        'is_reverse': True,
                        'is_protect': True
                    })
                    switch = switch.lstrip('[(')
                    switch = switch.rstrip(')]')
                    sub_switches = switch.split("/")
                    for tmp_sub_switch in sub_switches:
                        switch_name = tmp_sub_switch.strip()
                        if switch_name != "":
                            val = {
                                'index': data_index,
                                'is_reverse': True,
                                'is_protect': True,
                                'switch': switch_cache[switch_name.upper()]
                            }
                            sub_switch_infos.append((0, 0, val))
                elif switch.startswith('('):
                    val.update({
                        'is_reverse': True
                    })
                    switch = switch.lstrip('(')
                    switch = switch.rstrip(')')
                    sub_switches = switch.split("/")
                    for tmp_sub_switch in sub_switches:
                        switch_name = tmp_sub_switch.strip()
                        if switch_name != "":
                            val = {
                                'index': data_index,
                                'is_reverse': True,
                                'is_protect': False,
                                'switch': switch_cache[switch_name.upper()]
                            }
                            sub_switch_infos.append((0, 0, val))
                elif switch.startswith('['):
                    val.update({
                        'is_protect': True
                    })
                    switch = switch.lstrip('[')
                    switch = switch.rstrip(']')
                    sub_switches = switch.split("/")
                    for tmp_sub_switch in sub_switches:
                        switch_name = tmp_sub_switch.strip()
                        if switch_name != "":
                            val = {
                                'index': data_index,
                                'is_reverse': False,
                                'is_protect': True,
                                'switch': switch_cache[switch_name.upper()]
                            }
                            sub_switch_infos.append((0, 0, val))
                else:
                    # 普通
                    sub_switches = switch.split("/")
                    for tmp_sub_switch in sub_switches:
                        switch_name = tmp_sub_switch.strip()
                        if switch_name != "":
                            val = {
                                'index': data_index,
                                'is_reverse': False,
                                'is_protect': False,
                                'switch': switch_cache[switch_name.upper()]
                            }
                            sub_switch_infos.append((0, 0, val))

                val["switches"] = sub_switch_infos
                vals.append((0, 0, val))

            return vals

        def create_hostile_signal_info(row):
            '''
            创建道岔信息
            :param row:
            :return:
            '''
            vals = []
            signal_str = row[16]
            if not signal_str or signal_str.strip() == '':
                return vals

            # 先找出所有带条件的，取得所有的信号机
            signals = []
            condition_signal_ar = re.findall(r'\<.*?\>[^,]+', signal_str)
            for signal in condition_signal_ar:
                signal_str = signal_str.replace(str(signal), '')
                signals.append(signal)
            extra_ar = signal_str.split(',')
            signals += extra_ar

            for data_index, signal in enumerate(signals):
                if signal == '':
                    continue
                val = dict()
                if signal.startswith('<'):
                    reverse_index = signal.find('>')
                    condition_switches = signal[1: reverse_index]
                    condition_switch_ar = condition_switches.split(',')

                    condition_switch_vals = []
                    for condition_switch in condition_switch_ar:
                        switches = condition_switch.split("/")
                        for tmp_switch in switches:
                            tmp_switch_val = dict()
                            if tmp_switch.startswith('[('):
                                tmp_switch_val['is_reverse'] = True
                                tmp_switch_val['is_protect'] = True
                                tmp_switch = tmp_switch.lstrip('[(')
                                tmp_switch = tmp_switch.rstrip(')]')
                            elif condition_switch.startswith('('):
                                tmp_switch_val['is_reverse'] = True
                                tmp_switch_val['is_protect'] = False
                                tmp_switch = tmp_switch.lstrip('(')
                                tmp_switch = tmp_switch.rstrip(')')
                            elif tmp_switch.startswith('['):
                                tmp_switch_val['is_reverse'] = False
                                tmp_switch_val['is_protect'] = True
                                tmp_switch = tmp_switch.lstrip('[')
                                tmp_switch = tmp_switch.rstrip(']')
                            else:
                                tmp_switch_val['is_reverse'] = False
                                tmp_switch_val['is_protect'] = False

                            if tmp_switch not in switch_cache:
                                raise exceptions.ValidationError(
                                    '系统中没有{switch}数据'.format(switch=condition_switch))

                            tmp_switch_val['switch_id'] = switch_cache[tmp_switch]
                            condition_switch_vals.append(
                                (0, 0, tmp_switch_val))

                    if len(condition_switch_vals) > 0:
                        val['condition_switches'] = condition_switch_vals

                    condition_signal_str = signal[reverse_index + 1:]
                    condition_signal_array = condition_signal_str.split(' ')
                    for condition_signal in condition_signal_array:
                        try:
                            val['signal'] = signal_cache[condition_signal.rstrip(
                                'DdLl').upper()]
                            vals.append(val)
                        except Exception as e:
                            print('error')
                            raise e
                else:
                    val['signal'] = signal_cache[signal.rstrip('DdLl').upper()]
                    val['is_reverse'] = False
                    val['is_protect'] = False
                    val['condition_switch'] = False

            rst = []
            for val in vals:
                rst.append((0, 0, val))

            return rst

        def create_sec_info(row):
            '''
            创建道岔信息
            :param row:
            :return:
            '''
            secs_str = row[17]
            secs = secs_str.split(',')
            vals = []
            for index, sec in enumerate(secs):
                val = {
                    'index': index,
                }
                sec = sec.strip()
                if not sec or sec == '':
                    val['sec'] = False
                elif sec in sec_cache:
                    val['sec'] = sec_cache[sec]
                elif sec + 'G' in sec_cache:
                    val['sec'] = sec_cache[sec + 'G']
                else:
                    val['sec'] = False

                vals.append((0, 0, val))
            return vals

        def get_face_route(row):
            '''
            取得迎面过路，迎面进路的实质是一个区段
            :param row:
            :return:
            '''
            if row[18]:
                tmp_str = row[18].strip()
                if tmp_str:
                    tmp_str = tmp_str.replace("\n", "")
                    tmp_str = tmp_str.replace("\r", "")
                    return sec_cache[tmp_str]
            if row[19]:
                tmp_str = row[19].strip()
                tmp_str = tmp_str.replace("\n", "")
                tmp_str = tmp_str.replace("\r", "")
                if tmp_str:
                    return sec_cache[tmp_str]
            return False

        def get_other_interlock(row):
            '''
            取得其它(联锁) 第20列
            :param row:
            :return:
            '''
            return None

            if row[20]:
                tmp_str = row[20]
                tmp_str = tmp_str.strip()
                tmp_str = tmp_str.replace("\n", "")
                tmp_str = tmp_str.replace("\r", "")
                if tmp_str:
                    return other_interlock_cache[tmp_str]

        def get_route_type(row):
            '''
            取得进路类型
            :param row:
            :return:
            '''
            txt = row[0].strip()
            txt = txt.replace("\n", "")
            txt = txt.replace("\r", "")
            if txt == '列车进路':
                return 'train'
            else:
                return 'dispatch'

        # 处理进路
        table_val = {
            'location': self.location.id,
            'file_data': self.interlock_file,
            'file_name': self.file_name,
            'route_ids': []
        }

        for index, row in enumerate(rows):
            table_val['route_ids'].append((0, 0, {
                "index": int(row[3]),
                "location": self.location.id,
                "route_type": get_route_type(row),
                "direction": row[1],
                "route_sub_type": row[2].replace("\n", "").replace("\r", ""),
                "start_rail": sec_cache[row[9].strip()],
                "end_rail": sec_cache[row[10].strip()],
                "method": row[5],
                "origin_press_btn": row[6],
                "mdias_press_start": row[7],
                "mdias_press_end": row[8],
                "direction_switch": switch_cache[row[11]] if row[11] != '' else False,
                "signals_infos": create_signal_info(row),
                "switch_infos": create_switch_info(row),
                "switch_text": row[15],
                "hostile_signal_infos": create_hostile_signal_info(row),
                "hostile_signal_text": row[16],
                "sec_infos": create_sec_info(row),
                "sec_text": row[17],
                "face_route": get_face_route(row),
                "other_interlock": get_other_interlock(row)
            }))

        self.env['metro_park.interlock.table'].create(table_val)
