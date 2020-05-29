import logging
import traceback
from queue import Queue

from odoo.http import request
from odoo.models import SUPERUSER_ID
from .model import Log, LogField

_logger = logging.getLogger(__name__)


class LogManage(object):
    queue = Queue(maxsize=100)

    log = Log
    logfield = LogField

    OPERATION_TYPE_MAP = {}

    @classmethod
    def _push_log(cls, content='Record Change', res_id=None,
                  record=None, mode=None, error=None, fields=None,
                  module_name=None, ip=None, request_url=None,
                  user_id=None, user_login=None, user_name=None
                  ):
        try:
            model_name = getattr(record, '_name', None)
            model_description = getattr(record, '_description', None)
            table_name = getattr(record, '_table', None)
            mode_description = cls.OPERATION_TYPE_MAP.get(mode)
            log = Log.create(content=content, model_name=model_name,
                             model_description=model_description,
                             table_name=table_name, res_id=res_id,
                             module_name=module_name,
                             mode=mode, error=error,
                             mode_description=mode_description,
                             request_url=request_url,
                             ip=ip, user_id=user_id, user_login=user_login,
                             user_name=user_name
                             )
            if fields:
                field_list = [LogField(**dict(filed, log_id=log.id)) for filed in fields]
                LogField.bulk_create(field_list)

        except Exception as e:
            traceback.print_exc()

    @classmethod
    def where(cls, log_type=None, user_login=None, date_range=None):
        where = []
        if log_type:
            where.append((Log.mode == log_type))
        if user_login:
            where.append((Log.user_login.contains(user_login)))
        if date_range:
            where += [(Log.create_data >= date_range[0]), (Log.create_data <= date_range[1])]
        return where

    @classmethod
    def paginate(cls, page, items_per_page, log_type=None, user_login=None, date_range=None):
        where = cls.where(log_type, user_login, date_range)
        query = Log.select()
        if where:
            query = query.where(*where)
        return query.order_by(Log.create_data.desc()).paginate(page, items_per_page)

    @classmethod
    def query_field_by_log(cls, log_id):
        try:
            return LogField.select().where(LogField.log_id == log_id)
        except:
            _logger.error('query field log fail')
            return []

    @classmethod
    def handler(cls):
        while True:
            log = cls.queue.get()
            cls._push_log(**log)

    @classmethod
    def put_log(cls, **kwargs):
        try:
            if 'record' in kwargs:
                record = kwargs['record']
                env = record.env
            else:
                env = request.env
            user_id = env.user.id
            user_login = env.user.login
            user_name = env.user.name
        except RuntimeError:
            user_id = SUPERUSER_ID
            user_login = 'System'
            user_name = 'System'
        except Exception:
            import traceback
            traceback.print_exc()
            return False
        try:
            request_url = request.httprequest.url
            ip = request.httprequest.environ.get("REMOTE_ADDR", '')
        except:
            ip = None
            request_url = None

        cls.queue.put(dict(kwargs, request_url=request_url,
                           ip=ip,
                           user_id=user_id,
                           user_name=user_name,
                           user_login=user_login))

    @classmethod
    def register_type(cls, tag, description):

        if tag not in cls.OPERATION_TYPE_MAP:
            cls.OPERATION_TYPE_MAP[tag] = description
        else:
            raise ValueError('type already exits')
