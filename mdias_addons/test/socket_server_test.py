import socketio
import threading
import time
from datetime import datetime
import random

test_message_count = 100000
thread_num = 1


def task():
    thread_name = threading.current_thread().getName()
    sio = socketio.Client()
    sio.connect('http://172.16.108.55:9080')

    def send_message(msg, event=None):
        event = event or 'message'
        sio.emit(event, msg)

    @sio.event
    def connect():
        print('%s connection connected, %s' % (thread_name, datetime.now()))
        send_message('%s connected, %s' % (thread_name, datetime.now()))

    @sio.event
    def disconnect():
        print('%s disconnect, %s' % (thread_name, datetime.now()))

    @sio.event
    def test_message(msg):
        with open('./message.data', 'w+') as f:
            f.write(msg+"\n")
        print('get message \n: %s' % msg)

    for i in range(test_message_count):
        message = 'this %s, message index %s, time is %s' % (thread_name, i, datetime.now())
        print(message)
        send_message(message, event='test_message')
        time.sleep(random.randrange(0, 10)/10)
    sio.wait()


def start():
    for i in range(thread_num):
        print('start threading %s' % i)
        t = threading.Thread(target=task, name='th-%s' % i)
        t.start()


if __name__ == '__main__':
    start()


