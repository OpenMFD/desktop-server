from flask import (
    Blueprint,
)

bp = Blueprint(name='hello', import_name=__name__, url_prefix='/hello')


@bp.route('/')
def index():
    return "Hello World"
