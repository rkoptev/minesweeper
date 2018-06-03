import random

FIELD_SIZE_BEGINNER = (9, 9)
FIELD_SIZE_INTERMEDIATE = (16, 16)
FIELD_SIZE_EXPERT = (30, 16)
MINES_COUNT_BEGINNER = 10
MINES_COUNT_INTERMEDIATE = 40
MINES_COUNT_EXPERT = 99


class Minesweeper:
    """ This class handles the logic of playing one Minesweeper game. """

    def __init__(self, shape, mines_count: int, field_update_callback: callable, end_game_callback: callable):
        # Store parameters
        self.__shape = shape
        self.__mines_count = mines_count
        self.__field_update_callback = field_update_callback
        self.__end_game_callback = end_game_callback
        self.__game_active = True

        # Create empty game field (0 - empty space, 1 - mine)
        self.__field = [[0] * shape[0] for _ in range(shape[1])]

        # Create user view field (" " - undiscovered, "F" - flagged, "0" - empty, "1"-"8" - count of mines around,
        # "." - mine, "X" - false flagged mine, "*" - exploded mine)
        self.__player_view = [[" "] * shape[0] for _ in range(shape[1])]

        # Place mines randomly on field
        cells_count = shape[0] * shape[1]
        mines = random.sample(range(0, cells_count), mines_count)
        for mine in mines:
            mine_x = mine % shape[0]
            mine_y = mine // shape[0]
            self.__field[mine_y][mine_x] = 1

        self.__on_field_update()

    def mark_cell(self, coordinates) -> bool:
        """ Mark cell with flag, equivalent to right click on this cell """
        if not self.__game_active:
            return False
        x, y = coordinates

        # Only undiscovered cells can be marked
        if self.__player_view[y][x] == " ":
            self.__player_view[y][x] = "F"
            self.__on_field_update()
            return True
        # Return False if cell is already marked
        elif self.__player_view[y][x] == "F":
            return False

        return False

    def unmark_cell(self, coordinates) -> bool:
        if not self.__game_active:
            return False
        """ Remove marking flag from cell, equivalent to right click on marked cell """
        x, y = coordinates

        # Only undiscovered cells can be marked
        if self.__player_view[y][x] == "F":
            self.__player_view[y][x] = " "
            self.__on_field_update()
            return True
        # Return True if cell is already marked
        elif self.__player_view[y][x] == " ":
            return True

        return False

    def open_cell(self, coordinates) -> bool:
        if not self.__game_active:
            return False
        """ Open cell on field, equivalent to click on this cell """
        x, y = coordinates

        # If this is an empty cell:
        if self.__field[y][x] == 0:
            return self.__show_cell(coordinates)
        # If this is a cell with mine:
        elif self.__field[y][x] == 1:
            return self.__end_game(win=False, explosion=coordinates)

    def get_field(self):
        """ Return player field view """
        return list(self.__player_view)

    def get_shape(self) -> (int, int):
        """ Return shape of field in (x, y) format """
        return self.__shape

    def __show_cell(self, coordinates, propagation_call=False) -> bool:
        """ Open cell on field (internal method)"""
        x, y = coordinates

        # We can show only undiscovered cells (flagged cells can also be unflagged and discovered)
        if self.__player_view[y][x] in (" ", "F"):
            near_mines_count = self.__calculate_near_mines_count(coordinates)
            self.__player_view[y][x] = str(near_mines_count)

            if near_mines_count == 0:
                near_cells = self.__get_near_cells(coordinates)
                for cell in near_cells:
                    self.__show_cell(cell, propagation_call=True)

            if not propagation_call:
                self.__on_field_update()
            return True

        # Return false if action is not allowed
        return False

    def __check_end_game(self):
        """ Check if game is ended """
        for x in range(self.__shape[0]):
            for y in range(self.__shape[1]):
                if self.__field[y][x] == 0 and self.__player_view[y][x] in (" ", "F"):
                    return False

        self.__end_game(win=True)

    def __end_game(self, win=False, explosion=None):
        """ End game """
        for x in range(self.__shape[0]):
            for y in range(self.__shape[1]):

                # If cell was not opened
                if self.__player_view[y][x] == " ":
                    # If it's a mine
                    if self.__field[y][x] == 1:
                        self.__player_view[y][x] = "."
                    # If it's empty
                    else:
                        self.__player_view[y][x] = str(self.__calculate_near_mines_count((x, y)))

                # If cell was flagged
                elif self.__player_view[y][x] == "F":
                    # If it's a mine
                    if self.__field[y][x] == 1:
                        pass
                    # If it's empty
                    else:
                        self.__player_view[y][x] = "X"

                # If cell was opened - leave all as is

        # Mark exploded bomb
        if not win:
            self.__player_view[explosion[1]][explosion[0]] = "*"

        self.__on_end_game(win)

        self.__on_field_update()

        return True

    def __get_near_cells(self, coordinates):
        """ Return list of cells that are adjacent with specified one (left, right, top, bottom) """
        x, y = coordinates

        near_cells = []

        min_x = max(x - 1, 0)
        max_x = min(x + 1, self.__shape[0] - 1)
        min_y = max(y - 1, 0)
        max_y = min(y + 1, self.__shape[1] - 1)

        for i in range(min_x, max_x + 1):
            for j in range(min_y, max_y + 1):
                if not (i == x and j == y):
                    near_cells.append((i, j))

        return near_cells

    def __calculate_near_mines_count(self, coordinates) -> int:
        """ Return count of mines that are located around specified cell """
        near_cells = self.__get_near_cells(coordinates)

        mines_count = 0

        for cell in near_cells:
            mines_count += self.__field[cell[1]][cell[0]]

        return mines_count

    def calculate_flags_left(self) -> int:
        """ Return count of mines that supposed to be unflagged """
        flags_left = self.__mines_count

        for x in range(self.__shape[0]):
            for y in range(self.__shape[1]):
                if self.__player_view[y][x] == "F":
                    flags_left -= 1

        return flags_left

    def __on_end_game(self, win):
        """ Call player field view update callback to update players view """
        self.__end_game_callback(win)

    def __on_field_update(self):
        """ Call player field view update callback to update players view """
        self.__field_update_callback({
            "field": list(self.__player_view),
            "flags_left": self.calculate_flags_left()
        })
