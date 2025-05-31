from typing import Dict, List, Callable

import random
from enum import Enum


class NaC(object):

    class Levels(Enum):

        IDIOT = 0
        AVERAGE = 1
        GENIUS = 2

    def __init__(self, on_change:Callable, on_game_over:Callable):

        self.level = self.Levels.AVERAGE
        self._on_change = on_change
        self._on_game_over = on_game_over
        self._move_count = 0
        self._game_over = False
        self._win_paths = self.__create_win_paths()
        self._squares = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]]

    #--------------------------------------------------------------------
    # "PUBLIC" METHODS
    #--------------------------------------------------------------------

    def human_move(self, square:int) -> None:

        """
        To be called by UI when user makes move.
        square argument is number of square when
        arranged:
            1 2 3
            4 5 6
            7 8 9
        """

        if self._game_over != True:

            row_column = self.__get_row_column(square)

            if self._squares[row_column["row"]][row_column["column"]] == " ":

                self._squares[row_column["row"]][row_column["column"]] = "X"
                self._on_change(row_column["column"], row_column["row"], "X")

                self._move_count += 1

                if self.__check_for_winner() == False:
                    self.computer_move()


    def computer_move(self) -> None:

        """
        Called by this class after human_move, or
        called by UI to make computer start.
        """

        if self.level == self.Levels.IDIOT:
            self.__computer_move_idiot()
        elif self.level == self.Levels.AVERAGE:
            self.__computer_move_average()
        elif self.level == self.Levels.GENIUS:
            self.__computer_move_genius()

        self._move_count += 1

        self.__check_for_winner()


    def new_game(self) -> None:

        """
        Resets relevant attributes to start new game.
        """

        self._squares = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]]
        self._move_count = 0
        self._game_over = False


    def get_level_string(self) -> str:

        """
        Returns the current level as a human-readable string.
        """

        return self.Levels._member_names_[self.level.value]

    #--------------------------------------------------------------------
    # "PRIVATE" METHODS
    #--------------------------------------------------------------------

    def __computer_move_idiot(self) -> None:

        """
        Choose square at random
        """

        random.seed()

        while True:

            row = random.randint(0, 2)
            column = random.randint(0, 2)

            if self._squares[row][column] == " ":
                self._squares[row][column] = "O"
                self._on_change(column, row, "O")
                break


    def __computer_move_average(self) -> None:

        """
        Choose idiot or genius level
        at random with 50:50 probability
        """

        if random.randint(0, 1) == 0:
            self.__computer_move_idiot()
        else:
            self.__computer_move_genius()


    def __computer_move_genius(self) -> None:

        """
        Calculates the move most likely to
        result in a win.
        """

        # if first move of game use centre square
        # as this is in more win paths than other squares
        if self._move_count == 0:
            self._squares[1][1] = "O"
            self._on_change(1, 1, "O")
            return

        self.__populate_win_paths()

        # check if any moves give computer immediate win
        # 2 noughts and 1 empty
        for win_path in self._win_paths:
            if win_path["nought_count"] == 2 and win_path["empty_count"] == 1:
                empty_square = self.__find_empty_square(win_path)
                if empty_square != None:
                    self._squares[empty_square["row"]][empty_square["column"]] = "O"
                    self._on_change(empty_square["column"], empty_square["row"], "O")
                return

        # check if any moves give player immediate win
        # 2 crosses and 1 empty
        for win_path in self._win_paths:
            if win_path["cross_count"] == 2 and win_path["empty_count"] == 1:
                empty_square = self.__find_empty_square(win_path)
                if empty_square != None:
                    self._squares[empty_square["row"]][empty_square["column"]] = "O"
                    self._on_change(empty_square["column"], empty_square["row"], "O")
                return

        # check if any moves give computer potential win next go
        # 1 nought and 2 empty
        for win_path in self._win_paths:
            if win_path["nought_count"] == 1 and win_path["empty_count"] == 2:
                empty_square = self.__find_empty_square(win_path)
                if empty_square != None:
                    self._squares[empty_square["row"]][empty_square["column"]] = "O"
                    self._on_change(empty_square["column"], empty_square["row"], "O")
                return

        # check if any moves give player potential win next go
        # 1 cross and 2 empty
        for win_path in self._win_paths:
            if win_path["cross_count"] == 1 and win_path["empty_count"] == 2:
                empty_square = self.__find_empty_square(win_path)
                if empty_square != None:
                    self._squares[empty_square["row"]][empty_square["column"]] = "O"
                    self._on_change(empty_square["column"], empty_square["row"], "O")
                return

        # cannot find useful move so call
        # __computer_move_idiot to make random move
        self.__computer_move_idiot()


    def __get_row_column(self, square:int) -> Dict:

        """
        Get row and column numbers as dictionary
        for squares numbered:
        1 2 3
        4 5 6
        7 8 9
        """

        column = 0
        row = 0

        if square in [1,4,7]:
            column = 0
        elif square in [2,5,8]:
            column = 1
        else:
            column = 2

        if square in [1,2,3]:
            row = 0
        elif square in [4,5,6]:
            row = 1
        else:
            row = 2

        return {"row": row, "column": column}


    def __check_for_winner(self) -> bool:

        """
        Called after each move to check if there is a
        winner or if the game is over with no winner.
        """

        # check columns
        for column in range(0, 3):
            if self._squares[0][column] != " ":
                if self._squares[0][column] == self._squares[1][column] \
                and self._squares[0][column] == self._squares[2][column]:
                    self._on_game_over(self._squares[0][column])
                    self._game_over = True
                    return True

        # check rows
        for row in range(0, 3):
            if self._squares[row][0] != " ":
                if self._squares[row][0] == self._squares[row][1] \
                and self._squares[row][0] == self._squares[row][2]:
                    self._on_game_over(self._squares[row][0])
                    self._game_over = True
                    return True

        # check diagonals
        if self._squares[0][0] != " ":
            if self._squares[0][0] == self._squares[1][1] \
            and self._squares[0][0] == self._squares[2][2]:
                self._on_game_over(self._squares[0][0])
                self._game_over = True
                return True

        if self._squares[2][0] != " ":
            if self._squares[2][0] == self._squares[1][1] \
            and self._squares[2][0] == self._squares[0][2]:
                self._on_game_over(self._squares[0][2])
                self._game_over = True
                return True

        # draw if no winner but all 9 squares used
        if self._move_count == 9:
            self._on_game_over(" ")
            self._game_over = True
            return True

        # game not yet over
        return False


    def __create_win_paths(self) -> List:

        """
        Create list of the 8 win paths, each with a
        dictionary of:
            squares
            cross_count
            nought_count
            empty_count
        """

        win_paths = []

        # rows
        for row in range(0, 3):
            win_path = {"squares": [],
                        "cross_count": 0,
                        "nought_count": 0,
                        "empty_count": 0}

            for col in range(0, 3):
                win_path["squares"].append({"row": row,
                                           "column": col})

            win_paths.append(win_path)

        # columns
        for col in range(0, 3):
            win_path = {"squares": [],
                        "cross_count": 0,
                        "nought_count": 0,
                        "empty_count": 0}

            for row in range(0, 3):
                win_path["squares"].append({"row": row,
                                           "column": col})

            win_paths.append(win_path)

        # diagonals
        # top left -> bottom right
        win_path = {"squares": [],
                    "cross_count": 0,
                    "nought_count": 0,
                    "empty_count": 0}

        for row_col in range(0, 3):

            win_path["squares"].append({"row": row_col,
                                       "column": row_col})

        win_paths.append(win_path)

        # top right -> bottom left
        win_path = {"squares": [],
                    "cross_count": 0,
                    "nought_count": 0,
                    "empty_count": 0}

        for row in range(0, 3):

            win_path["squares"].append({"row": row,
                                       "column": 2 - row})

        win_paths.append(win_path)

        return win_paths


    def __populate_win_paths(self) -> None:

        """
        Set the totals of each win path.
        """

        for win_path in self._win_paths:

            win_path["cross_count"] = 0
            win_path["nought_count"] = 0
            win_path["empty_count"] = 0

            for square in win_path["squares"]:
                if self._squares[square["row"]][square["column"]] == " ":
                    win_path["empty_count"] += 1
                elif self._squares[square["row"]][square["column"]] == "X":
                    win_path["cross_count"] += 1
                elif self._squares[square["row"]][square["column"]] == "O":
                    win_path["nought_count"] += 1


    def __find_empty_square(self, win_path:Dict) -> Dict:

        """
        Finds an empty square in the given win paths
        for computer's next move.
        """

        for square in win_path["squares"]:
            if self._squares[square["row"]][square["column"]] == " ":
                return {"row": square["row"], "column": square["column"]}

        return None
