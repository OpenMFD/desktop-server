import json
import time
from pprint import pprint

import keyboard

# with open('bindings.json') as f:
#     data = json.load(f)
#
# action = data['spaceship_general']['v_exit']

# pprint(action)


def run():
    self_destruct()
    eject()


def self_destruct():
    for i in range(3):
        keyboard.press('alt+backspace')
        time.sleep(0.1)

    keyboard.release('alt+backspace')


def eject():
    keyboard.press_and_release('alt+f')


run()
