import os

from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.instance_path = os.path.abspath(app.instance_path+'/../../instance')

    db_path = os.path.join(app.instance_path, 'mfd-server.sqlite')
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
        # store the database in the instance folder
        DATABASE=db_path,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return 'Hello you!'

    from openmfd.server import hello

    # apply the blueprints to the app
    app.register_blueprint(hello.bp)
    # app.register_blueprint(mouse.bp)

    # make url_for('index') == url_for('blog.index')
    app.add_url_rule('/', endpoint='index')

    socketio.init_app(app)

    return app
