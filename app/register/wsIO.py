from flask_socketio import SocketIO

socketio = SocketIO()


def register_SocketIO(app):
    socketio.init_app(app, cors_allowed_origins="*")
