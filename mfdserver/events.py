from enum import Enum


class Events(Enum):
    # Used to monitor clients connecting, will dispatch available screens.
    CONNECT = 'connect'

    # Used to monitor clients disconnecting.
    DISCONNECT = 'disconnect'

    # Used to join screens, will dispatch the screen state as a response, and subscribe the client
    # to actions that happen within the screen.
    JOIN_SCREEN = 'join_screen'

    # Used to leave a screen and prevent updates for it being pushed to the client.
    LEAVE_SCREEN = 'leave_screen'

    # Used to run an action on the host
    RUN_ACTION = 'run_action'

    # Used to set the screen state
    SET_SCREEN_STATE = 'set_screen_state'
