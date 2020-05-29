
from odoo import models, fields, api, exceptions
from pprint import pprint
from odoo.exceptions import Warning, RedirectWarning
from odoo.tools import config
import itertools

if config.options.get('local_debug', False):
    from ...metro_park_dispatch.models.data_test import park_train_back_conditions_map
else:
    from ...metro_park_dispatch.models.data import park_train_back_conditions_map


class InterLockRouteTest(models.TransientModel):
    '''
    排路测试
    '''

    _name = 'metro_park.interlock.route_test'
    _description = '联锁表测试'
    _track_log = True

    def get_default_location(self):
        line_records = self.env['metro_park_base.line'].search([])
        if line_records:
            line_code = line_records[0].code
            rtu_name = park_train_back_conditions_map[line_code]['park_list'][0]['rtu_name']
            return self.env.ref('metro_park_base_data_%s.%s' % (line_code, rtu_name)).id
        return None

    @api.onchange('location', 'types')
    def get_pos_doamin(self):
        if not self.location:
            return {
                "domain": {
                    "start_pos": [],
                    "end_pos": []
                }
            }

        domain = {
            'start_pos': [('location', '=', self.location.id)],
            'end_pos': [('location', '=', self.location.id)]
        }

        if self.types == 'back_plan':
            domain['start_pos'].append(
                ('rail_type', '=', self.env.ref('metro_park_base.rail_type_exchange').id))
        elif self.types == 'out_plan':
            domain['end_pos'].append(
                ('rail_type', '=', self.env.ref('metro_park_base.rail_type_exchange').id))

        return {
            "domain": domain
        }

    location = fields.Many2one(string="所属场段",
                               comodel_name="metro_park_base.location", default=get_default_location)

    types = fields.Selection(string='类型', requried=True, selection=[
        ('back_plan', '接车'),
        ('out_plan', '发车'),
        ('train_dispatch', '调车')], default='train_dispatch')

    start_pos = fields.Many2one(
        string="起点", comodel_name="metro_park_base.rails_sec", domain=get_pos_doamin)
    end_pos = fields.Many2one(
        string="终点", comodel_name="metro_park_base.rails_sec",  domain=get_pos_doamin)

    def on_interlock_route_test(self):
        '''
        测试按钮
        '''

        if not self.start_pos or not self.end_pos:
            raise exceptions.Warning('请选择起始股道')

        if self.types == 'train_dispatch':
            routes = self.env["metro_park.interlock.route"].search_dispatch_route(
                self.location.id, self.start_pos, self.end_pos)
        else:
            routes = self.env["metro_park.interlock.route"].search_train_plan_route(
                self.location.id, self.start_pos, self.end_pos, self.types)

        log_str = ""
        for route in routes:
            for item in route:
                log_str += "{start_rail}->{end_rail} ".format(
                    start_rail=item.start_rail.no, end_rail=item.end_rail.no)
            print("\n------>>>", log_str, "\n")
        if log_str:
            raise exceptions.Warning('找到路径: %s' % (log_str))
        else:
            raise exceptions.Warning('未找到路径')

    def on_interlock_route_group_test(self):
        def get_sec(sec_no):
            return self.env['metro_park_base.rails_sec'].search([
                ('no', '=', sec_no),
                ('location', '=', 2)
            ])

        def show_routes(start_rail, end_rail, routes):
            print("========== ", start_rail.no,
                  " -> ", end_rail.no, " ==========")
            for route in routes:
                log_str = ""
                for item in route:
                    log_str += "{start_rail}->{end_rail} ".format(
                        start_rail=item.start_rail.no, end_rail=item.end_rail.no)
                print("\n------>>>", log_str, "\n")

        a_rail = []
        b_rail = []
        normal_rail = []
        normal_out_rail = []  # 可收发车的非AB股
        exchange_rail = []  # 转换轨
        pull_out_rail = []  # 牵出线

        location_name = self.location.alias
        # banqiao
        if location_name == 'banqiao':
            a_rail = ["21AG", "22AG", "23AG", "24AG", "25AG", "26AG",
                      "27AG", "28AG", "29AG", "30AG", "31AG", "32AG"]
            b_rail = ["21BG", "22BG", "23BG", "24BG", "25BG", "26BG",
                      "27BG", "28BG", "29BG", "30BG", "31BG", "32BG"]
            normal_rail = ["10G", "11G", "12G", "13G", "14G",
                           "15G", "16G", "17G", "18G", "19G", "20G", "D67G"]
            normal_out_rail = ["33G", "34G", "35G", "36G", "37G", "38G", "39G"]
            exchange_rail = ["T1701G", "T1714G"]
            pull_out_rail = ["D7G", "D5G", "D1G", "D37G"]
        elif location_name == 'gaodalu':
            a_rail = ["5AG", "6AG", "7AG", "8AG", "9AG", "10AG",
                      "11AG", "12AG", "13AG", "14AG", "15AG", "16AG"]
            b_rail = ["5BG", "6BG", "7BG", "8BG", "9BG", "10BG",
                      "11BG", "12BG", "13BG", "14BG", "15BG", "16BG"]
            normal_rail = ["1G", "D22G"]
            normal_out_rail = ["2G", "3G", "4G", "23G", "24G", "25G"]
            exchange_rail = ["T2602G", "T2617G"]
            pull_out_rail = ["D2G", "D4G"]
        elif location_name == 'pitong':
            a_rail = []
            b_rail = []
            normal_rail = ["1G", '51G', '52G', '53G', '54G',
                           '55G', '56G', '57G', '58G', '61G', 'D30G']
            normal_out_rail = ['2G', '3G', '4G', '5G', '6G', '7G', '8G', '9G', '10G', '11G', '12G', '13G', '14G', '15G', '16G', '17G', '18G', '19G', '20G', '21G', '22G', '23G', '24G', '25G',
                               '26G', '27G', '28G', '29G', '30G', '31G', '32G', '33G', '34G', '35G', '36G', '37G', '38G', '39G', '40G', '41G', '42G', '43G', '44G', '45G', '46G', '47G', '48G', '49G', '50G']
            exchange_rail = ["T1126G", "T1101G"]
            pull_out_rail = ["D2G", "D4G"]
        elif location_name == 'huilong':
            a_rail = ["4AG", "5AG", "6AG", "7AG", "8AG", "9AG", "10AG", "11AG", "12AG", "13AG",
                      "14AG", "15AG", "16AG", "17AG", "18AG", "19AG", "20AG", "21AG", "22AG", "23AG", "24AG"]
            b_rail = ["4BG", "5BG", "6BG", "7BG", "8BG", "9BG", "10BG", "11BG", "12BG", "13BG",
                      "14BG", "15BG", "16BG", "17BG", "18BG", "19BG", "20BG", "21BG", "22BG", "23BG", "24BG"]
            normal_rail = ["29G", "L0515DGJF"]
            normal_out_rail = ["1G", "2G", "3G", "25G", "26G", "27G", "28G"]
            exchange_rail = ["T6602G", "T6617G"]
            pull_out_rail = ["D1G"]
        elif location_name == 'longdengshan':
            a_rail = ['7AG', '8AG', '9AG', '10AG', '11AG', '12AG', '13AG', '14AG', '15AG', '16AG', '17AG',
                      '18AG', '19AG', '20AG', '21AG', '22AG', '23AG', '24AG', '25AG', '26AG', '27AG', '28AG']

            b_rail = ['7BG', '8BG', '9BG', '10BG', '11BG', '12BG', '13BG', '14BG', '15BG', '16BG', '17BG',
                      '18BG', '19BG', '20BG', '21BG', '22BG', '23BG', '24BG', '25BG', '26BG', '27BG', '28BG']

            normal_rail = ["1G", "6G", "29G"]
            normal_out_rail = ['2G', '3G', '4G', '5G', "30G", "31G"]
            exchange_rail = ["T4621", "T4617"]
            pull_out_rail = ["D1G", "D3G"]
        elif location_name == 'yuanhua':
            pass
        else:
            raise exceptions.Warning('未知的场段%s' % (location_name))
        self.group_test(a_rail, b_rail, normal_rail,
                        normal_out_rail, exchange_rail, pull_out_rail)

    def group_test(self, a_rail, b_rail, normal_rail, normal_out_rail, exchange_rail, pull_out_rail):
        import itertools
        # 收车 exchange_rail -> a_rail,normal_out_rail
        all_routes = list(itertools.product(
            exchange_rail, a_rail + normal_out_rail))
        self.search_route(all_routes, "back_plan")

        # 发车 a_rail,normal_out_rail  -> exchange_rail
        all_routes = list(itertools.product(
            a_rail + normal_out_rail, exchange_rail))
        self.search_route(all_routes, "out_plan")

        # 调车 a_rail -> b_rail  b_rail -> a_rail a_rail,normal_rail,normal_out_rail -> a_rail,normal_rail,normal_out_rail
        all_routes = list(itertools.product(a_rail, b_rail))
        all_routes += list(itertools.product(b_rail, a_rail))
        all_routes += list(itertools.product(a_rail +
                                             normal_rail + normal_out_rail, a_rail +
                                             normal_rail + normal_out_rail))
        self.search_route(all_routes, "train_dispatch")

    def search_route(self, all_routes, type):
        print('test all routes for', type)
        for route in all_routes:
            if route[0] != route[1]:
                start_rail = self.env['metro_park_base.rails_sec'].search(
                    [('no', '=', route[0]), ('location', '=', self.location.id)])
                end_rail = self.env['metro_park_base.rails_sec'].search(
                    [('no', '=', route[1]), ('location', '=', self.location.id)])
                if not start_rail or not end_rail:
                    print(route, '区段不存在')

                if type == 'train_dispatch':
                    routes = self.env["metro_park.interlock.route"].search_dispatch_route(
                        self.location.id, start_rail, end_rail)
                else:
                    routes = self.env["metro_park.interlock.route"].search_train_plan_route(
                        self.location.id, start_rail, end_rail, type)

                for route in routes:
                    log_str = ""
                    for item in route:
                        log_str += "{start_rail}->{end_rail} ".format(
                            start_rail=item.start_rail.no, end_rail=item.end_rail.no)
                    print("\n------>>>", log_str, type, "\n")

    def on_interlock_route_clear_cache_route(self):
        self.env['interlock_table.route_cache'].search(
            [('location', '=', self.location.id)]).unlink()
