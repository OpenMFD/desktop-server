import json
import os
import time

import keyboard

with open(os.path.abspath(os.path.dirname(__file__) + "/../../toolset/starcitizen") + '/bindings.json') as f:
    data = json.load(f)

starcitizen_keybinding_map = {
    '0': '0',
    '1': '1',
    '2': '2',
    '3': '3',
    '4': '4',
    '5': '5',
    '6': '6',
    '7': '7',
    '8': '8',
    '9': '9',
    'a': 'a',
    'b': 'b',
    'c': 'c',
    'd': 'd',
    'e': 'e',
    'f': 'f',
    'g': 'g',
    'h': 'h',
    'i': 'i',
    'j': 'j',
    'k': 'k',
    'l': 'l',
    'm': 'm',
    'n': 'n',
    'o': 'o',
    'p': 'p',
    'q': 'q',
    'r': 'r',
    's': 's',
    't': 't',
    'u': 'u',
    'v': 'v',
    'w': 'w',
    'x': 'x',
    'y': 'y',
    'z': 'z',

    'comma': ',',
    'lbracket': '[',
    'period': '.',
    'rbracket': ']',
    'slash': '/',

    'np_0': 'np_0',  # TODO: WORK OUT THE NUM PAD
    'np_1': 'np_1',  # TODO: WORK OUT THE NUM PAD
    'np_2': 'np_2',  # TODO: WORK OUT THE NUM PAD
    'np_3': 'np_3',  # TODO: WORK OUT THE NUM PAD
    'np_4': 'np_4',  # TODO: WORK OUT THE NUM PAD
    'np_5': 'np_5',  # TODO: WORK OUT THE NUM PAD
    'np_6': 'np_6',  # TODO: WORK OUT THE NUM PAD
    'np_7': 'np_7',  # TODO: WORK OUT THE NUM PAD
    'np_8': 'np_8',  # TODO: WORK OUT THE NUM PAD
    'np_9': 'np_9',  # TODO: WORK OUT THE NUM PAD
    'np_add': 'np_add',  # TODO: WORK OUT THE NUM PAD
    'np_divide': 'np_divide',  # TODO: WORK OUT THE NUM PAD
    'np_multiply': 'np_multiply',  # TODO: WORK OUT THE NUM PAD
    'np_period': 'np_period',  # TODO: WORK OUT THE NUM PAD
    'np_subtract': 'np_subtract',  # TODO: WORK OUT THE NUM PAD

    'backspace': 'backspace',
    'end': 'end',
    'enter': 'enter',
    'escape': 'escape',
    'hmd_pitch': 'hmd_pitch',
    'hmd_roll': 'hmd_roll',
    'hmd_yaw': 'hmd_yaw',
    'home': 'home',
    'lalt': 'alt',
    'insert': 'insert',
    'lctrl': 'left ctrl',
    'lshift': 'left shift',
    'pgdn': 'page up',
    'pgup': 'page down',
    'rctrl': 'right ctrl',
    'rshift': 'right shift',
    'space': 'space',
    'tab': 'tab',

    'down': 'down',
    'left': 'left',
    'right': 'right',
    'up': 'up',

    'maxis_x': 'maxis_x',
    'maxis_y': 'maxis_y',
    'maxis_z': 'maxis_z',
    'mwheel_down': 'mwheel_down',
    'mwheel_up': 'mwheel_up',

    'f1': 'f1',
    'f2': 'f2',
    'f3': 'f3',
    'f4': 'f4',
    'f5': 'f5',
    'f6': 'f6',
    'f7': 'f7',
    'f8': 'f8',
    'f9': 'f9',
    'f10': 'f10',
    'f11': 'f11',
    'f12': 'f12',
}


def run_action(name):
    action = data[name]

    # TODO: This should be separated into on_press and on_release so we can
    # simulate "hold" keybindings properly.
    activation_mode: str = action['activation_mode']

    if activation_mode is None or activation_mode == "all":
        print(f"No activation mode for {name}. Defaulting to press")
        activation_mode = 'press'

    keyboard_binding: str = action['device']['keyboard']

    if keyboard_binding is None or keyboard_binding.strip() == "":
        print(f"No keyboard mapping for {name}.")
        return

    keys_to_run = keyboard_binding.split("+")

    hotkey = ""

    for key in keys_to_run:
        key = starcitizen_keybinding_map[key.lower()]

        if hotkey != "":
            hotkey += "+"

        hotkey += key

    print(f"Running {hotkey} on machine")

    if activation_mode in ["press", "tap", "double_tap"]:
        keyboard.press_and_release(hotkey)

        if activation_mode == "double_tap":
            time.sleep(0.1)
            keyboard.press_and_release(hotkey)

    if activation_mode == "delayed_press":
        for i in range(3):
            keyboard.press(hotkey)
            time.sleep(0.1)

        keyboard.release(hotkey)
