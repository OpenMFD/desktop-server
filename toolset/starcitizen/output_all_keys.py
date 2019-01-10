import json
from pprint import pprint

with open('bindings.json') as f:
    data = json.load(f)

keys = []

for binding_key in data:
    action = data[binding_key]

    name: str = action['action_name']
    keyboard: str = action['device']['keyboard']

    if keyboard is None or keyboard.strip() == "":
        # print(f"No keyboard mapping for {name}.")
        continue

    keys_to_run = keyboard.split("+")

    for key in keys_to_run:
        key = key.lower()

        if key not in keys:
            keys.append(key)

keys.sort()

pprint(keys)
