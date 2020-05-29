import logging

from odoo.models import BaseModel

_logger = logging.getLogger(__name__)


def trigger_up_event(self, event_name, data, to=None, room=None,
                     callback_name=None, model_name=None, res_id=None, **kwargs):
    '''
        触发bus消息，通过事件名称进行区分
        :param self:
        :param event_name:
        :param data:
        :param to:
        :param callback_name:
        :param model_name:
        :param res_id:
        :param room: 房间号
        :return:
    '''
    _logger.info('%s trigger up event %s' % (self.env.user.login, event_name))
    if isinstance(res_id, (int,)):
        res_id = [res_id]
    if model_name is None:
        model_name = self._name
    msg = _make_bus_message(self.env, data, event_name, to=to, room=room, callback_name=callback_name,
                            model_name=model_name,
                            res_ids=res_id, **kwargs)

    self.env['funenc.socket_io'].trigger_event_to_client(msg)


def _make_bus_message(env, data, event_name, to=None,
                      room=None,
                      callback_name=None,
                      model_name=None,
                      res_ids=None, **kwargs):
    """
        :param data:响应事件的数据
        :param to: 如果省略to消息将会采用广播方式发送到当前在线所有用户
        :param callback_name: 消息回调前端事件成功回调方法名，如果失败将会函数将会传入False
        :param event_name: 响应的事件名
        :param res_ids 如存在会根据记录id执行回调
        :return:
    """

    data = {
        'uid': to,
        'room': room,
        'event_type': event_name,
        'data': {
            'context': str(env.context),
            'data': data
        }
    }
    if callback_name:
        data.update({
            'callback_info': {
                'model': model_name,
                'ids': res_ids,
                'kwargs': kwargs,
                'name': callback_name,
                'uid': env.user.id
            }
        })

    return data


BaseModel.trigger_up_event = trigger_up_event
