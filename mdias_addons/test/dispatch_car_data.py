import odoo
from odoo.tools import config
from odoo.models import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
import time
import os
import random

path = os.path.abspath(os.path.dirname(__file__))
args = ['-c', './local.conf', '-d', 'mdias2',  '--addons-path',
        '%s,%s' % (os.path.abspath(os.path.join(path, '../../', './%s' % 'mdias_addons')),
                   os.path.abspath(os.path.join(path, '../../', './%s' % 'addons')))]
config.parse_config(args)
config.parse_config(args)

db_name = config['db_name']

date_range = ['2019-08-01', '2019-09-05']

DATA_MAX = 10000

DAY_SECOND = 24*60*60
DISPATCH_STATE = ['draft', 'wait_accept', 'accepted',
                          'wait_executing',  'executing', 'rebacked', 'canceled', 'finished']


def make_data(local_vars):
    print('start create record')
    env = local_vars['env']
    model_name = 'metro_park_dispatch.dispatch_request'
    obj = env[model_name]
    user_ids = [49]
    department_ids = env['funenc.wechat.department'].search([]).ids
    routes = env['metro_park.interlock.route'].search([])
    rail_tracks = []
    for route in routes:
        rail_tracks.append((route.start_rail.id, route.end_rail.id))
    dev_ids = env['metro_park_dispatch.cur_train_manage'].search([]).ids
    start_unixtime = int(time.mktime(time.strptime(date_range[0], DEFAULT_SERVER_DATE_FORMAT))) - 8*60*60
    end_unixtime = int(time.mktime(time.strptime(date_range[1], DEFAULT_SERVER_DATE_FORMAT))) - 8*60*60
    day_range = range(start_unixtime, end_unixtime, DAY_SECOND)
    for i in range(1, DATA_MAX+1):
        start_track, end_track = random.choice(rail_tracks)

        user_id = random.choice(user_ids)
        div_id = random.choice(dev_ids)
        day = random.choice(day_range)
        day_range = [day, day + DAY_SECOND]
        request_data = random.randint(*day_range)
        dispatch_time = [random.randint(request_data,  day + DAY_SECOND), random.randint(request_data,  day + DAY_SECOND)]
        start_dispatch_date = min(dispatch_time)
        end_dispatch_date = max(dispatch_time)
        notice_time = random.randint(end_dispatch_date, day + DAY_SECOND)
        value = {
            'state': random.choice(DISPATCH_STATE),
            'train': div_id,
            'dispatch_date': datetime.fromtimestamp(day),
            'start_time': datetime.fromtimestamp(start_dispatch_date),
            'finish_time': datetime.fromtimestamp(end_dispatch_date),
            'dispatch_type': random.choice(['own', 'other_train']),
            'source_rail': end_track,
            'target_rail': start_track,
            'uid': user_id,
            'disconnecting_off': random.choice([True, False]),
            'rail_grounded': random.choice([True, False]),
            'rail_is_incursion': random.choice([True, False]),
            'prohibition_battery_power': random.choice([True, False]),
            'place_iron_shoes': random.choice([True, False]),
            'suspension_is_normal': random.choice([True, False]),
        }

        record = obj.create(value)
        try:
            record.make_dispatch_detail()
            record.notice_id.write({
                'dispatch_driver': random.choice(user_ids),
                'park_dispatcher': random.choice(department_ids),
                'dispatch_group': random.choice(department_ids),
                'notice_time': datetime.fromtimestamp(notice_time),
            })
            print('>>>create cmd')
            record.open_dispatch_detail_action()

        except Exception as e:
            print(e.args)
            import traceback
            traceback.print_exc()
        finally:
            obj.env.cr.commit()
        print('make data value %s' % i)
    print('make finished')


def start():

    with odoo.api.Environment.manage():
        local_vars = {
            'openerp': odoo,
            'odoo': odoo,
        }
        if db_name:
            registry = odoo.registry(db_name)
            with registry.cursor() as cr:
                uid = odoo.SUPERUSER_ID
                ctx = odoo.api.Environment(cr, uid, {})['res.users'].context_get()
                env = odoo.api.Environment(cr, uid, ctx)
                local_vars['env'] = env
                local_vars['self'] = env.user
                print('make data')
                make_data(local_vars)
                print(env)
        else:
            print('db name not exits')


if __name__ == '__main__':
    start()
