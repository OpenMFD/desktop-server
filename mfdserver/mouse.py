import math
import random
import time
import autopy
from flask import Blueprint

from mfdserver import socketio

bp = Blueprint(name='mouse', import_name=__name__, url_prefix='/mouse')

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


@socketio.on('move-mouse')
def mouse_move():
    sine_mouse_wave()


@bp.route('/move')
def index():
    sine_mouse_wave()
    return "Mouse has been moved!"
