import autopy
import math
import time
import random
from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app)

    app.run(
        host="0.0.0.0",
        port=6789
    )

TWO_PI = math.pi * 2.0


def sine_mouse_wave():
    """
    Moves the mouse in a sine wave from the left edge of
    the screen to the right.
    """
    width, height = autopy.screen.size()
    height /= 2
    height -= 10  # Stay in the screen bounds.

    for x in range(int(width)):
        y = int(height * math.sin((TWO_PI * x) / width) + height)
        autopy.mouse.move(x, y)
        time.sleep(random.uniform(0.001, 0.003))


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@socketio.on('move-mouse')
def handle_message():
    sine_mouse_wave()

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/move-mouse")
def move_mouse():
    sine_mouse_wave()
    return "Mouse has been moved!"


