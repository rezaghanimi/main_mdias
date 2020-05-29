import datetime
from contextlib import closing
from peewee import *
from pytz import timezone

from odoo.models import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.sql_db import db_connect
from odoo.tools import config

db_name = config.get('operation_log_db', 'operation_log_db')
db_host = config.get('db_host')
db_port = config.get('db_port')
db_password = config.get('db_password')
db_user = config.get('db_user')
cst_tz = timezone('Asia/Shanghai')


def init_database():
    try:
        # 判断是否能够链接该数据库
        db_connect(db_name).cursor().close()
    except Exception:
        db_connect('postgres')
        with closing(db_connect('postgres').cursor()) as cr:
            cr.autocommit(True)
            cr.execute(
                """CREATE DATABASE "%s" ENCODING 'unicode' TEMPLATE "%s" """ % (db_name, config['db_template']))
            cr.commit()


init_database()
database = PostgresqlDatabase(db_name, user=db_user,
                              password=db_password,
                              host=db_host,
                              port=db_port, autocommit=True, autorollback=True)


class BaseModel(Model):
    class Meta:
        database = database


class Log(BaseModel):
    mode = CharField()
    request_url = TextField(null=True)
    user_name = CharField(null=True)
    user_id = IntegerField(null=True)
    user_login = CharField(null=True)
    model_name = CharField(null=True)
    res_id = IntegerField(null=True)
    description = TextField(null=True)
    create_data = DateTimeField(default=lambda: datetime.datetime.now(tz=cst_tz).
                                strftime(DEFAULT_SERVER_DATETIME_FORMAT))
    error = TextField(null=True)
    model_description = TextField(null=True)
    ip = IPField(null=True)
    device = CharField(null=True)
    content = TextField(null=True)
    table_name = CharField(null=True)
    mode_description = CharField(null=True)
    module_name = CharField(null=True)
    fields = DeferredForeignKey('LogField', deferrable='INITIALLY DEFERRED', null=True)


class LogField(BaseModel):
    log_id = ForeignKeyField(Log, deferrable='INITIALLY DEFERRED')
    filed_name = CharField()
    filed_display = CharField()
    old_value = TextField(null=True)
    new_value = TextField(null=True)
    field_type = CharField()


database.create_tables([Log, LogField])
