import random
import sys

FIELD_SIZE_BEGINNER = (9, 9)
FIELD_SIZE_INTERMEDIATE = (16, 16)
FIELD_SIZE_EXPERT = (30, 16)
MINES_COUNT_BEGINNER = 10
MINES_COUNT_INTERMEDIATE = 40
MINES_COUNT_EXPERT = 99


class Field:
    """ This class handles the logic of playing one Minesweeper game. """
    def __init__(self, shape, mines_count: int, field_update_callback: callable):
        # Store parameters
        self.__shape = shape
        self.__mines_count = mines_count
        self.__field_update_callback = field_update_callback

        # Create empty game field (0 - empty space, 1 - mine)
        self.__field = [[0] * shape[0] for _ in range(shape[1])]

        # Create user view field (" " - undiscovered, "F" - flagged, "0" - empty, "1"-"8" - count of mines around,
        # "." - mine, "X" - false flagged mine, "*" - exploded mine)
        self.__user_view = [[" "] * shape[0] for _ in range(shape[1])]

        # Place mines randomly on field
        cells_count = shape[0] * shape[1]
        mines = random.sample(range(0, cells_count), mines_count)
        for mine in mines:
            mine_y = mine % shape[0]
            mine_x = mine // shape[0]
            self.__field[mine_y][mine_x] = 1

        self.__on_field_update()

    def mark_cell(self, coordinates) -> bool:
        """ Mark cell with flag, equivalent to right click on this cell """
        x, y = coordinates

        # Only undiscovered cells can be marked
        if self.__user_view[y][x] == " ":
            self.__user_view[y][x] = "F"
            self.__on_field_update()
            return True
        # Return True if cell is already marked
        elif self.__user_view[y][x] == "F":
            return True

        return False

    def unmark_cell(self, coordinates) -> bool:
        """ Remove marking flag from cell, equivalent to right click on marked cell """
        x, y = coordinates

        # Only undiscovered cells can be marked
        if self.__user_view[y][x] == "F":
            self.__user_view[y][x] = " "
            self.__on_field_update()
            return True
        # Return True if cell is already marked
        elif self.__user_view[y][x] == " ":
            return True

        return False

    def open_cell(self, coordinates) -> bool:
        """ Open cell on field, equivalent to click on this cell """
        x, y = coordinates

        # If this is an empty cell:
        if self.__field[y][x] == 0:
            return self.__show_cell(coordinates)
        # If this is a cell with mine:
        elif self.__field[y][x] == 1:
            return self.__game_over(coordinates)

    def __show_cell(self, coordinates, propagation_call=False) -> bool:
        """ Open cell on field (internal method)"""
        x, y = coordinates

        # We can show only undiscovered cells (flagged cells can also be unflagged and discovered)
        if self.__user_view[y][x] in (" ", "F"):
            near_mines_count = self.__calculate_near_mines_count(coordinates)
            self.__user_view[y][x] = str(near_mines_count)

            if near_mines_count == 0:
                near_cells = self.__get_near_cells(coordinates)
                for cell in near_cells:
                    self.__show_cell(cell, propagation_call=True)

            if not propagation_call:
                self.__on_field_update()
            return True

        # Return false if action is not allowed
        return False

    def __game_over(self, coordinates):
        """ End game and reveal all the field to player """
        for x in range(self.__shape[0]):
            for y in range(self.__shape[1]):

                # If cell was not opened
                if self.__user_view[y][x] == " ":
                    # If it's a mine
                    if self.__field[y][x] == 1:
                        self.__user_view[y][x] = "."
                    # If it's empty
                    else:
                        self.__user_view[y][x] = str(self.__calculate_near_mines_count((x, y)))

                # If cell was flagged
                elif self.__user_view[y][x] == "F":
                    # If it's a mine
                    if self.__field[y][x] == 1:
                        pass
                    # If it's empty
                    else:
                        self.__user_view[y][x] = "X"

                # If cell was opened - leave all as is

        # Mark exploded bomb
        self.__user_view[coordinates[1]][coordinates[0]] = "*"

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

    def __on_field_update(self):
        """ Call view update callback to update players view """
        self.__field_update_callback(list(self.__user_view))


def field_pretty_print(f):
    sys.stdout.write("██" * (len(f[0]) + 2))
    sys.stdout.write("\n")
    for line in f:
        sys.stdout.write("█ ")
        for cell in line:
            sys.stdout.write(cell + " ")
        sys.stdout.write("█ \n")
    sys.stdout.write("██" * (len(f[0]) + 2) + "\n")


if __name__ == "__main__":
    # from minesweeper import *
    field = Field(FIELD_SIZE_BEGINNER, MINES_COUNT_BEGINNER, field_pretty_print)
    field.open_cell((0, 0))
