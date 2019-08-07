import curses

import nac


class NaCConsole(object):

    def __init__(self):

        self.screen = curses.initscr()
        curses.curs_set(False)
        curses.noecho()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)

        self.game = nac.NaC(on_change=self.on_game_changed,
                            on_game_over=self.on_game_over)

        self.__draw_board()
        self.__show_level()

        self.__event_loop()

    def __event_loop(self):

        while True:

            key = self.screen.getch()

            if key in range(49, 58):
                self.game.human_move(int(key) - 48)
            elif chr(key) == "x":
                curses.endwin()
                exit()
            elif chr(key) == "s":
                self.game.computer_move()
            elif chr(key) == "i":
                self.game.level = self.game.Levels.IDIOT
                self.__show_level()
            elif chr(key) == "a":
                self.game.level = self.game.Levels.AVERAGE
                self.__show_level()
            elif chr(key) == "g":
                self.game.level = self.game.Levels.GENIUS
                self.__show_level()
            elif chr(key) == "n":
                self.game.new_game()
                self.__draw_board()
                self.__show_level()

    def __draw_board(self):

        self.screen.clear()

        width = 56

        row1 = "                  |                  |                  \n"
        row2 = "------------------|------------------|------------------\n"

        def draw_rows_1():
            for r in range(0, 9):
                self.screen.addstr(row1, curses.color_pair(1) | curses.A_BOLD)

        draw_rows_1()
        self.screen.addstr(row2, curses.color_pair(1) | curses.A_BOLD)
        draw_rows_1()
        self.screen.addstr(row2, curses.color_pair(1) | curses.A_BOLD)
        draw_rows_1()

        x = 0
        y = 0
        s = 1

        for h in range(0, 3):
            for v in range(0, 3):
                self.screen.addstr(y, x, str(s), curses.color_pair(1) | curses.A_BOLD)
                x += 19
                s += 1
            x = 0
            y += 10

        self.screen.addstr(30, 0, " Computer start     s".ljust(width, " "),
                           curses.color_pair(2) | curses.A_BOLD)
        self.screen.addstr(31, 0, " Place an X         1-9".ljust(width, " "),
                           curses.color_pair(2) | curses.A_BOLD)
        self.screen.addstr(32, 0, " Idiot              i".ljust(width, " "),
                           curses.color_pair(2) | curses.A_BOLD)
        self.screen.addstr(33, 0, " Average            a".ljust(width, " "),
                           curses.color_pair(2) | curses.A_BOLD)
        self.screen.addstr(34, 0, " Genius             g".ljust(width, " "),
                           curses.color_pair(2) | curses.A_BOLD)
        self.screen.addstr(35, 0, " New game           n".ljust(width, " "),
                           curses.color_pair(2) | curses.A_BOLD)
        self.screen.addstr(36, 0, " Exit               x".ljust(width, " "),
                           curses.color_pair(2) | curses.A_BOLD)

        self.screen.refresh()

    def __show_level(self):

        width = 56

        level_string = " Current level:     {}".format(self.game.get_level_string(), width=width)
        level_string += " " * (56 - len(level_string))
        self.screen.addstr(29, 0, level_string, curses.color_pair(2) | curses.A_BOLD)
        self.screen.refresh()

    def on_game_changed(self, column, row, shape):

        x = 2 + (19 * column)
        y = 1 + (10 * row)

        if(shape == "X"):
            self.screen.addstr(y + 0, x, "XX          XX", curses.color_pair(1) | curses.A_BOLD)
            self.screen.addstr(y + 1, x, "  XX      XX  ", curses.color_pair(1) | curses.A_BOLD)
            self.screen.addstr(y + 2, x, "    XX  XX    ", curses.color_pair(1) | curses.A_BOLD)
            self.screen.addstr(y + 3, x, "      XX      ", curses.color_pair(1) | curses.A_BOLD)
            self.screen.addstr(y + 4, x, "    XX  XX    ", curses.color_pair(1) | curses.A_BOLD)
            self.screen.addstr(y + 5, x, "  XX      XX  ", curses.color_pair(1) | curses.A_BOLD)
            self.screen.addstr(y + 6, x, "XX          XX", curses.color_pair(1) | curses.A_BOLD)
        elif(shape == "O"):
            self.screen.addstr(y + 0, x, "      OO     ", curses.color_pair(1) | curses.A_BOLD)
            self.screen.addstr(y + 1, x, "    OO  OO   ", curses.color_pair(1) | curses.A_BOLD)
            self.screen.addstr(y + 2, x, "  OO      OO ", curses.color_pair(1) | curses.A_BOLD)
            self.screen.addstr(y + 3, x, " OO        OO", curses.color_pair(1) | curses.A_BOLD)
            self.screen.addstr(y + 4, x, "  OO      OO ", curses.color_pair(1) | curses.A_BOLD)
            self.screen.addstr(y + 5, x, "    OO  OO   ", curses.color_pair(1) | curses.A_BOLD)
            self.screen.addstr(y + 6, x, "      OO     ", curses.color_pair(1) | curses.A_BOLD)

        self.screen.refresh()

    def on_game_over(self, winner):

            width = 56
            message_width = 18

            if winner == "X":
                winner_string = "You won".center(message_width, " ")
            elif winner == "O":
                winner_string = "The computer won".center(message_width, " ")
            else:
                winner_string = "Game ended in draw".center(message_width, " ")

            self.screen.addstr(13, 19, " " * message_width, curses.color_pair(3) | curses.A_BOLD)
            self.screen.addstr(14, 19, winner_string, curses.color_pair(3) | curses.A_BOLD)
            self.screen.addstr(15, 19, " " * message_width, curses.color_pair(3) | curses.A_BOLD)

            self.screen.refresh()


cons = NaCConsole()
