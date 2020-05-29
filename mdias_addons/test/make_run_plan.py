import odoo
from odoo.tools import config
from odoo.models import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime
import time
import os
import random

path = os.path.abspath(os.path.dirname(__file__))
args = ['-c', '../local.conf', '-d', 'mdias2',  '--addons-path',
        '%s,%s' % (os.path.abspath(os.path.join(path, '../../', './%s' % 'mdias_addons')),
                   os.path.abspath(os.path.join(path, '../../', './%s' % 'addons')))]
config.parse_config(args)

db_name = config['db_name']

date_range = ['2019-08-01', '2019-09-05']

DATA_MAX = 50

DAY_SECOND = 24*60*60
DISPATCH_STATE = ['draft', 'wait_accept', 'accepted',
                          'wait_executing',  'executing', 'rebacked', 'canceled', 'finished']


def make_data(local_vars):
    env = local_vars['env']
    model_name = 'metro_park_dispatch.day_run_plan'
    obj = env[model_name]
    train_ids = env['metro_park_dispatch.train_out_plan'].search([('id', '>', 0)]).mapped('train_id').ids
    for i in range(1, DATA_MAX+1):
        train_id = random.choice(train_ids)
        out_plan_ids = env['metro_park_dispatch.train_out_plan'].\
            search([('train_id', '=', train_id)]).ids
        out_plan = env['metro_park_dispatch.train_out_plan'].browse(random.choice(out_plan_ids))
        back_plan = env['metro_park_dispatch.train_back_plan'].\
            search([('train_id', '=', train_id)], limit=1)

        value = {
            'train': train_id,
            'date': out_plan.date,
            'train_back_plan': back_plan.id,
            'train_out_plan': out_plan.id,
            'wash': random.choice([True, False])
        }
        obj.create(value)
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
                make_data(local_vars)
                print(env)
                cr.commit()
        else:
            print('db name not exits')


if __name__ == '__main__':
    start()
