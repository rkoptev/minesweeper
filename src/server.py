import logging as log
import eventlet.wsgi
import socketio
from flask import Flask, render_template

from src.minesweeper import *

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
    """ Socket.io namespace for dashboard """
    def on_connect(self, sid, environ):
        log.info("Watcher %s connected" % sid)
        self.update(sid)

    @staticmethod
    def update(sid=None):
        fields = []
        for sid in games:
            fields.append({
                "name": names[sid] or "Anonymous",
                "field": games[sid].get_field(),
                "flags_left": games[sid].calculate_flags_left()
            })

        sio.emit("state", namespace="/watch", sid=sid, data={
            "fields": fields
        })


class PlayerNamespace(socketio.Namespace):
    """ Socket.io namespace for players """
    def on_connect(self, sid, environ):
        log.info("Player connected, sid=%s" % sid)
        self.enter_room(sid, room=sid)

    def on_play(self, sid, data):
        names[sid] = data["name"]
        log.info("Player %s started %s game, sid=%s" % (names[sid], data["difficulty"], sid))
        if data["difficulty"] == "beginner":
            games[sid] = Minesweeper(FIELD_SIZE_BEGINNER, MINES_COUNT_BEGINNER,
                                     lambda field: self.field_update_callback(sid, field),
                                     lambda win: self.end_game_callback(sid, win))
        elif data["difficulty"] == "intermediate":
            games[sid] = Minesweeper(FIELD_SIZE_INTERMEDIATE, MINES_COUNT_INTERMEDIATE,
                                     lambda field: self.field_update_callback(sid, field),
                                     lambda win: self.end_game_callback(sid, win))
        elif data["difficulty"] == "expert":
            games[sid] = Minesweeper(FIELD_SIZE_EXPERT, MINES_COUNT_EXPERT,
                                     lambda field: self.field_update_callback(sid, field),
                                     lambda win: self.end_game_callback(sid, win))

    def on_mark(self, sid, data):
        # Check if game started
        if sid not in games:
            return

        if "coordinates" not in data:
            self.emit("message", room=sid, data="You submitted wrong turn")
            return

        coordinates = data["coordinates"]
        
        if not self.__check_coordinates(sid, coordinates):
            return

        if games[sid].mark_cell(coordinates):
            log.info("Player %s marking cell with coordinates [%d,%d], sid=%s" % (names[sid], coordinates[0], coordinates[1], sid))
        else:
            self.emit("message", room=sid, data="Cell with coordinates [%d, %d] is already marked or opened" % (coordinates[0], coordinates[1]))

    def on_unmark(self, sid, data):
        # Check if game started
        if sid not in games:
            return

        if "coordinates" not in data:
            self.emit("message", room=sid, data="You submitted wrong turn")
            return

        coordinates = data["coordinates"]
        if not self.__check_coordinates(sid, coordinates):
            return

        if games[sid].unmark_cell(coordinates):
            log.info("Player %s unmarking cell with coordinates [%d,%d], sid=%s" % (names[sid], coordinates[0], coordinates[1], sid))
        else:
            self.emit("message", room=sid, data="Cell with coordinates [%d, %d] is not marked or already opened" % (coordinates[0], coordinates[1]))

    def on_open(self, sid, data):
        # Check if game started
        if sid not in games:
            return

        if "coordinates" not in data:
            self.emit("message", room=sid, data="You submitted wrong turn")
            return

        coordinates = data["coordinates"]
        if not self.__check_coordinates(sid, coordinates):
            return

        if games[sid].open_cell(coordinates):
            log.info("Player %s open cell with coordinates [%d,%d], sid=%s" % (names[sid], coordinates[0], coordinates[1], sid))
        else:
            self.emit("message", room=sid, data="Cell with coordinates [%d, %d] is already opened" % (coordinates[0], coordinates[1]))

    def __check_coordinates(self, sid, coordinates):
        # Get coordinates of cell
        x, y = coordinates

        # Check type
        if type(x) != int or type(y) != int:
            self.emit("message", room=sid, data="Coordinates must be integers from 0 to field_size - 1")
            return False

        # Check if coordinates are in range of field
        if not 0 <= x < games[sid].get_shape()[0] or not 0 <= y < games[sid].get_shape()[1]:
            self.emit("message", room=sid, data="Coordinates [%d, %d] are out of field boundaries" % (coordinates[0], coordinates[1]))
            return False

        return True

    def field_update_callback(self, sid, data):
        # Update user field
        self.emit("update", room=sid, data=data)
        # Update watchers UI
        WatcherNamespace.update()

    def end_game_callback(self, sid, win):
        if win:
            log.info("Player %s win the game" % names[sid])
        else:
            log.info("Player %s lose the game" % names[sid])

        self.emit("end_game", {"win": win}, room=sid)

    @staticmethod
    def on_disconnect(sid):
        if sid in names:
            del names[sid]

        if sid in games:
            del games[sid]


if __name__ == '__main__':
    # Configure logger
    log.basicConfig(level=log.INFO)

    # Register namespaces fo Socket.io
    sio.register_namespace(WatcherNamespace("/watch"))
    sio.register_namespace(PlayerNamespace("/play"))

    # Wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # Deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8154)), app)
