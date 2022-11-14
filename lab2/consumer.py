import threading
from flask import Flask, request
from producer import *
import time
import json

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

server3 = Flask(__name__)

# https://superfastpython.com/thread-safe-list/

class ThreadSafeList():
    def __init__(self):
        self._list = list()
        self._lock = threading.Lock()
 
    def append(self, value):
        with self._lock:
            self._list.append(value)
 
    def pop(self):
        with self._lock:
            return self._list.pop()

oven = ThreadSafeList()

@server3.route('/consumer', methods=['POST'])
def consumer():
    oven.append(json.loads(request.data))
    return ""

class Cooker(threading.Thread):
    def __init__(self, thread_name):
        threading.Thread.__init__(self)
        self.thread_name = thread_name

    def run(self):
        while True:
            try:
                received_potato = oven.pop()["data"]
                received_potato[0] = fries_emoji
                received_potato[1] = cooked
                requests.post(url='http://localhost:5020/aggregator/received', json={"data" : received_potato})
                print(f'Thread -- {Colors.CYAN}{self.thread_name}{Colors.END} -- sent [{received_potato[0]} {Colors.GREEN}{received_potato[1]}{Colors.END}] {received_potato[2]}')
            except IndexError:
                print("Oven is still empty...")

            time.sleep(2)

if __name__ == '__main__':

    threading.Thread(target=lambda: server3.run(port=5030, host="0.0.0.0", debug=False)).start()

    for index in range(1, 6):
        x = Cooker(thread_name=f'Cooker_{index}')
        x.start()