from mfdserver import socketio
from mfdserver.events import Events


@socketio.on(Events.CONNECT.value)
def connect():
    print('A client connected')


@socketio.on(Events.DISCONNECT.value)
def disconnect():
    print('A client disconnected')


@socketio.on(Events.JOIN_SCREEN.value)
def join_screen(data):
    print('A client requested to join a screen', data)


@socketio.on(Events.LEAVE_SCREEN.value)
def leave_screen(data):
    print('A client requested to leave a screen', data)


@socketio.on(Events.RUN_ACTION.value)
def run_action(data):
    from mfdserver.actions.runner import run_action as exec_action

    print('A client requested to run an action', data)

    exec_action(data['name'])
