import threading
import requests
from flask import Flask, request
import time
import random

# https://stackoverflow.com/questions/14888799/disable-console-messages-in-flask-server

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# DISABLE POST DEBUGGING

uncooked = "uncooked"
cooked = "cooked"
potato_emoji = "🥔"
fries_emoji = "🍟"

# https://gist.github.com/rene-d/9e584a7dd2935d0f461904b9f2950007

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

server1 = Flask(__name__)

@server1.route('/producer', methods=['POST'])
def producer():
    return "Success"

# https://realpython.com/intro-to-python-threading/

class Worker(threading.Thread):
    def __init__(self, thread_name):
        threading.Thread.__init__(self)
        self.thread_name = thread_name

    def run(self):
        while True:
            new_potato = list([potato_emoji, uncooked, str(random.randint(100, 999))])

            try:
                requests.post(url='http://localhost:5002/consumer', json={"data" : new_potato})
                print(f'Thread -- {Colors.YELLOW}{self.thread_name}{Colors.END} -- sent [{new_potato[0]} {Colors.LIGHT_RED}{new_potato[1]}{Colors.END}] {new_potato[2]}')

            except requests.exceptions.ConnectionError:
                print ("Consumer server is not up...")

            time.sleep(2)

if __name__ == '__main__':

    threading.Thread(target=lambda: server1.run(port=5001, host="0.0.0.0", debug=False)).start()

    for index in range(1, 5 + 1):
        x = Worker(thread_name=f'Worker_{index}')
        x.start()