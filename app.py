"""
app.py
"""

from argparse import ArgumentParser

from flask import Flask

app = Flask(__name__)

app.config.from_pyfile('config.py', silent=True)

with app.app_context():
    from util import init_db
    from controllers import *

    init_db()

if __name__ == "__main__":
    argParser = ArgumentParser(
        usage = "Usage: python3 " + __file__ + " [--host <host>] [--port <port>] [--help]"
    )
    argParser.add_argument("--host", default="0.0.0.0", help="host")
    argParser.add_argument("-p", "--port", default=8080, help="port")
    argParser.add_argument("-d", "--debug", default=False, help="debug")
    options = argParser.parse_args()

    app.run(host=options.host , port=options.port, debug=options.debug)
