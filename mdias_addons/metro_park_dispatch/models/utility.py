
# -*- coding: utf-8 -*-

import pendulum


def datetime_to_str(records):
    '''
    处理时间
    :return: 
    '''
    for record in records:
        for key in record:
            if type(record[key]).__name__ in ['datetime', 'date']:
                record[key] = str(record[key])
    return records


def time_str_to_int(time_str):
    '''
    时间转换数值表示
    :return:
    '''
    tmp = pendulum.parse(time_str)
    return tmp.hour * 60 * 60 + tmp.minute * 60 + tmp.second


def get_now_time_int_repr():
    '''
    取得当前时间的整数代表
    :return:
    '''
    now = pendulum.now('UTC').add(hours=8)
    return now.hour * 60 * 60 + now.minute * 60 + now.second


def time_int_to_time(val):
    '''
    取得当前时间的整数代表
    :return:
    '''
    is_next_day = False
    if val > 24 * 3600:
        is_next_day = True
        val = val - 24 * 3600

    hour = int(val / 3600)
    minute = int((val - hour * 3600) / 60)
    second = val - hour * 3600 - minute * 60
    time_str = '{hour:0>2}:{minute:0>2}:{second:0>2}'\
        .format(hour=hour, minute=minute, second=second)
    return {
        "next_day": is_next_day,
        "time": time_str
    }
