import json
import xml.etree.ElementTree

def run():
    lang = parse_lang()

    bindings = parse_default_profile(lang)
    bindings = parse_layout(bindings, 'data/layout_keyboard_advanced.xml')
    bindings = flatten(bindings)

    write_bindings(bindings)

    print("Done. Written to bindings.json")


def parse_lang():
    lang = {}

    with open('data/en.ini', encoding='utf-8-sig') as fp:
        for line in fp:
            parsed_string = line.split('=', 1)
            lang[parsed_string[0].strip()] = parsed_string[1].strip()

    return lang


def parse_default_profile(lang):
    bindings = {}
    root = xml.etree.ElementTree.parse('data/defaultProfile.xml').getroot()

    for child in root:
        if child.tag != 'actionmap':
            continue

        action_map_name = child.attrib['name']

        for action in child:
            action_name = action.attrib['name']
            keyboard = get_key_if_exists('keyboard', action.attrib)
            mouse = get_key_if_exists('mouse', action.attrib)
            xboxpad = get_key_if_exists('xboxpad', action.attrib)
            joystick = get_key_if_exists('joystick', action.attrib)
            activation_mode = get_key_if_exists('ActivationMode', action.attrib)
            label = None
            description = None

            if 'UILabel' in action.attrib and action.attrib['UILabel'][1:] in lang:
                description = lang[action.attrib['UILabel'][1:]]
            if 'UIDescription' in action.attrib and action.attrib['UIDescription'][1:] in lang:
                description = lang[action.attrib['UIDescription'][1:]]

            if action_map_name not in bindings:
                bindings[action_map_name] = {}

            bindings[action_map_name][action_name] = {
                'action_name': action_name,
                'action_map_name': action_map_name,
                'activation_mode': activation_mode,
                'label': label,
                'description': description,
                'device': {
                    'keyboard': keyboard,
                    'mouse': mouse,
                    'xboxpad': xboxpad,
                    'joystick': joystick,
                }
            }

    return bindings


def parse_layout(bindings, file):
    root = xml.etree.ElementTree.parse(file).getroot()

    for child in root:
        if child.tag != 'actionmap':
            continue

        action_map_name = child.attrib['name']

        if action_map_name not in bindings:
            continue

        for action in child:
            action_name = action.attrib['name']

            if action_name not in bindings[action_map_name]:
                continue

            for rebind in action:
                device = rebind.attrib['device']
                input = rebind.attrib['input']
                activation_mode = get_key_if_exists('ActivationMode', rebind.attrib)

                bindings[action_map_name][action_name]['device'][device] = input

                if activation_mode is not None:
                    bindings[action_map_name][action_name]['activation_mode'] = activation_mode

    return bindings


def write_bindings(bindings):
    with open('bindings.json', 'w') as fp:
        json.dump(bindings, fp, indent="  ")


def get_key_if_exists(needle, haystack):
    if needle in haystack:
        return haystack[needle]

    return None


def flatten(bindings):
    flat = {}

    for group_name, binding_group in iter(bindings.items()):
        for binding_name, binding in iter(binding_group.items()):
            flat[group_name + "." + binding_name] = binding

    return flat


run()
