import eventlet.wsgi
import socketio
from flask import Flask, render_template
from minesweeper import *

sio = socketio.Server()
app = Flask(__name__)

# Game instances (identifier is the sid)
games = {}
# Player names (identifier is the sid)
names = {}


@app.route('/')
def index():
    """Serve the client-side application."""
    return render_template('index.html')


class WatcherNamespace(socketio.Namespace):
    def on_connect(self, sid, environ):
        print("watcher %s connected" % sid)
        self.update(sid)

    @staticmethod
    def update(sid=None):
        fields = {}
        for sid in games:
            fields[sid] = {
                "name": names[sid] or "Anonymous",
                "field": games[sid].get_field()
            }

        sio.emit("state", namespace="/watch", sid=sid, data={
            "fields": fields
        })


class PlayerNamespace(socketio.Namespace):
    def on_connect(self, sid, environ):
        print("player %s connected" % sid)
        self.enter_room(sid, room=sid)

    def on_play(self, sid, data):
        print("player %s started %s game" % (sid, data["difficulty"]))
        names[sid] = data["name"]
        if data["difficulty"] == "beginner":
            games[sid] = Minesweeper(FIELD_SIZE_BEGINNER, MINES_COUNT_BEGINNER,
                                     lambda field: self.field_update_callback(sid, field),
                                     lambda win: self.end_game_callback(sid, win))
        elif data["difficulty"] == "intermediate":
            games[sid] = Minesweeper(FIELD_SIZE_INTERMEDIATE, MINES_COUNT_INTERMEDIATE,
                                     lambda field: self.field_update_callback(sid, field),
                                     lambda win: self.end_game_callback(sid, win))
        elif data["difficulty"] == "intermediate":
            games[sid] = Minesweeper(FIELD_SIZE_EXPERT, MINES_COUNT_EXPERT,
                                     lambda field: self.field_update_callback(sid, field),
                                     lambda win: self.end_game_callback(sid, win))

    @staticmethod
    def on_mark(sid, data):
        if sid not in games:
            return
        coordinates = data["coordinates"]
        print("player %s marking cell with coordinates (%d,%d)" % (sid, coordinates[0], coordinates[1]))
        games[sid].mark_cell(coordinates)

    @staticmethod
    def on_unmark(sid, data):
        if sid not in games:
            return
        coordinates = data["coordinates"]
        print("player %s unmarking cell with coordinates (%d,%d)" % (sid, coordinates[0], coordinates[1]))
        games[sid].unmark_cell(coordinates)

    @staticmethod
    def on_open(sid, data):
        if sid not in games:
            return
        coordinates = data["coordinates"]
        print("player %s open cell with coordinates (%d,%d)" % (sid, coordinates[0], coordinates[1]))
        games[sid].open_cell(coordinates)

    def field_update_callback(self, sid, field):
        # Update user field
        self.emit("update", room=sid, data={
            "field": field
        })
        # Update watchers UI
        WatcherNamespace.update()

    def end_game_callback(self, sid, win):
        if win:
            print("player %s win the game" % sid)
        else:
            print("player %s lose the game" % sid)

        self.emit("end_game", {"win": win}, room=sid)

    @staticmethod
    def on_disconnect(sid):
        if sid in names:
            del names[sid]

        if sid in games:
            del games[sid]


if __name__ == '__main__':
    # Register namespaces fo Socket.io
    sio.register_namespace(WatcherNamespace("/watch"))
    sio.register_namespace(PlayerNamespace("/play"))

    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8154)), app)
