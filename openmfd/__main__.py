import os
import ssl
from multiprocessing import Process

from flask import Flask

from openmfd.server import create_app, socketio
from openmfd.ssl.generate import generate_instance_ssl

app = create_app()


def main():
    has_certificate = os.path.isfile(app.instance_path + "/cert.pem")
    if not has_certificate:
        generate_instance_ssl(app.instance_path)

    run_server(app)

    # process = Process(target=run_server, args=(app,))
    # process.start()


def run_server(app: Flask):
    keyfile = app.instance_path + "/key.pem"
    certfile = app.instance_path + "/cert.pem"

    # ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # ctx.load_cert_chain(
    #     certfile,
    #     keyfile,
    # )

    socketio.run(
        app,
        debug=True,
        use_reloader=False,
        host='0.0.0.0',
        port=6789,
        ssl_version=ssl.PROTOCOL_TLSv1_2,
        keyfile=keyfile,
        certfile=certfile,
    )


main()
