import threading
import requests
from flask import Flask, request
import time
import random
import json

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class Colors:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"

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

    # return the number of items in the list
    def length(self):
        # acquire the lock
        with self._lock:
            return len(self._list)

aggregator_list = ThreadSafeList()
received_list = ThreadSafeList()

server2 = Flask(__name__)

@server2.route('/aggregator', methods=['POST'])
def aggregator():
    aggregator_list.append(json.loads(request.data))
    return "Success"

@server2.route('/aggregator/received', methods=['POST'])
def received():
    received_list.append(json.loads(request.data))
    return "Success"

class Aggregator(threading.Thread):
    def __init__(self, thread_name):
        threading.Thread.__init__(self)
        self.thread_name = thread_name

    def run(self):
        while True:
            try:
                received_potato = aggregator_list.pop()["data"]

                if received_potato[2] == 'aggregate':
                    received_potato[2] = 'delivery'

                    try:
                        requests.post(url='http://localhost:5030/consumer', json={"data" : received_potato})
                        print(f'Thread -- {Colors.YELLOW}{self.thread_name}{Colors.END} -- sent [{received_potato[0]} {Colors.LIGHT_RED}{received_potato[1]}{Colors.END}] {received_potato[2]}')

                    except requests.exceptions.ConnectionError:
                        print ("Consumer server is not up...")
            except IndexError:
                print("Aggregator list is still empty...")
            
            try:
                received_potato_delivery = received_list.pop()["data"]

                try:
                    requests.post(url='http://localhost:5010/producer', json={"data" : received_potato_delivery})
                    print(f'Delivery made of {received_potato_delivery[0]}')

                except requests.exceptions.ConnectionError:
                    print ("Producer server is not up...")
            except IndexError:
                print("Received list is still empty...")

            time.sleep(2)


if __name__ == '__main__':

    threading.Thread(target=lambda: server2.run(port=5020, host="0.0.0.0", debug=False)).start()

    for index in range(1, 6):
        x = Aggregator(thread_name=f'Aggregator_{index}')
        x.start()