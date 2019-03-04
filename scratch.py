import time
import random
import curses
import art
from collections import namedtuple
from thiefs_knapsack_items import knapsack_items


class ThiefsKnapsack:
    def __init__(self, num_items=5, capacity=10):
        items = []
        item = namedtuple('item', ('name', 'value', 'weight'))
        for _ in range(num_items):
            new_item = item(
                random.choice(knapsack_items),
                random.randrange(5, 100, 5),
                random.randrange(1, 6),)
            items.append(new_item)

        self.items = items
        self.capacity = capacity
        self.matrix = [[None] * (self.capacity + 1) for _ in self.items]
        self.call_stack = []
        self.call_count = 0

    def optimize_booty(self, window):
        V = self.matrix

        def _optimize_booty(i, j, window):
            self.call_count += 1
            self.call_stack.append([i, j, self.call_count])

            if i < 0:
                return 0

            self.print_matrix(i, j, window)
            if V[i][j] is None:
                without_item_i = _optimize_booty(i-1, j, window)
                with_item_i = (0 if self.items[i].weight > j else(
                    self.items[i].value + _optimize_booty(i-1, j-self.items[
                    i].weight, window)))

                V[i][j] = max(with_item_i, without_item_i)
                self.print_matrix(i, j, window)

            return V[i][j]

        optimal_booty = _optimize_booty(len(self.items)-1, self.capacity,
                                        window)
        return optimal_booty

    def print_matrix(self, i, j, window):
        window.clear()

        # Make it fun.
        self.print_title(window)

        # Get window height and width.
        w_height, w_width = window.getmaxyx()

        # Start stringify-ing matrix.
        top_row = ' ' * 20
        for capacity in range(self.capacity + 1):
            top_row += str(capacity).center(8)

        # Get matrix width and height.
        m_width = len(top_row)
        m_height = len(self.matrix)

        # Centering calculations.
        y_start = ((w_height - m_height) // 5) * 4
        x_start = (w_width - m_width) // 2

        # Left-align inventory with V matrix.
        self.print_inventory(i, x_start, window)

        # Add column headers.
        window.attron(curses.A_UNDERLINE)
        window.addstr(y_start, x_start, top_row)
        y_start += 1
        window.attroff(curses.A_UNDERLINE)


        # Build rest of matrix. Look for current cell in matrix and 2 cells
        # from previous row which will be called recursively if they do not
        # have values.
        cur_cell_yx, without_item_i_yx, with_item_i_yx = None, None, None
        for si, row in enumerate(self.matrix):
            row_text = str(self.items[si].name).ljust(20)
            for sj, cell in enumerate(row):
                # Current cell coordinates.
                if si == i and sj == j:
                    cur_cell_yx = (y_start, x_start+len(row_text))

                # without_item_i cell coordinates.
                elif si == i-1 and sj == j:
                    without_item_i_yx = (y_start, x_start+len(row_text))

                # with_item_i cell coordinates.
                elif si == i-1 and sj == j-self.items[i].weight:
                    with_item_i_yx = (y_start, x_start+len(row_text))

                cell_text = '|' + str(cell).center(6) + '|'
                row_text += cell_text

            window.addstr(y_start, x_start, row_text)
            y_start += 1

        # Highlight current cell.
        y, x = cur_cell_yx
        cur_cell_text = '|' + str(self.matrix[i][j]).center(6) + '|'
        window.attron(curses.A_STANDOUT)
        window.attron(curses.color_pair(1))
        window.addstr(y, x, cur_cell_text)
        window.attroff(curses.A_STANDOUT)
        window.attroff(curses.color_pair(1))

        # Highlight cell without_item_i
        if without_item_i_yx:
            y, x = without_item_i_yx
            without_item_i_text = '|' + str(self.matrix[i-1][j]).center(6) + '|'
            window.attron(curses.A_BLINK)
            window.addstr(y, x, without_item_i_text)
            window.attroff(curses.A_BLINK)

        # Highlight cell with_item_i
        if with_item_i_yx:

            y, x = with_item_i_yx
            with_item_i_text = '|' + str(self.matrix[i - 1][j-self.items[i].weight]).center(6) + '|'
            window.attron(curses.A_BLINK)
            window.addstr(y, x, with_item_i_text)
            window.attroff(curses.A_BLINK)

        # Add border, print to screen.
        window.border()
        window.refresh()
        time.sleep(1)
        return

    def print_inventory(self, i, x_start, window):
        '''Window is cleared and refreshed in self.print_matrix().'''
        # Get window height and width.
        w_height, w_width = window.getmaxyx()

        # Start stringify-ing matrix.
        top_row = 'Items' + (' ' * 15) + ' Weight ' + ' Value '

        # Get matrix width and height.
        m_width = len(top_row)
        m_height = len(self.items)

        # Centering calculations. Top 1/3 of screen.
        y_start = ((w_height - m_height) // 5) * 3
        #x_start = (w_width - m_width) // 2

        # Add column headers.
        window.attron(curses.A_UNDERLINE)
        window.addstr(y_start, x_start, top_row)
        y_start += 1
        window.attroff(curses.A_UNDERLINE)

        # Write the inventory list.
        for item_idx, item in enumerate(self.items):
            name, value, weight = item
            if item_idx == i:
                cur_item_yx = (y_start, x_start)
            row_text = name.ljust(20) + str(weight).center(8) + str(
                value).center(8)
            window.addstr(y_start, x_start, row_text)
            y_start += 1

        # Highlight current cell.
        y, x = cur_item_yx
        cur_item_text = str(self.items[i].name).ljust(20)
        window.attron(curses.A_STANDOUT)
        window.attron(curses.color_pair(1))
        window.addstr(y, x, cur_item_text)
        window.attroff(curses.A_STANDOUT)
        window.attroff(curses.color_pair(1))

    def print_title(self, window):
        app_title = art.text2art("Thief's Knapsack", font='basic')
        window.addstr(2, 0, app_title)


def greeting(stdscr):
    k = 0

    # Clear and refresh the screen for a blank canvas.
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses.
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Specify window size. Get height and width for use as variables.
    curses.resize_term(50, 150)
    HEIGHT, WIDTH = stdscr.getmaxyx()

    title = "Welcome to the Thief's Knapsack"
    subtitle = "Written by Kevin Hynes"

    start_x_title = int((WIDTH // 2) - (len(title) // 2) - len(title) % 2)
    start_x_subtitle = int((WIDTH // 2) - (len(subtitle) // 2) - len(subtitle)
                           % 2)
    start_y_title = int((HEIGHT // 2) - 2)
    start_y_subtitle = start_y_title  + 1


    # Start drawing the opening screen.
    stdscr.border()
    title_string = ''
    stdscr.attron(curses.color_pair(1))
    stdscr.attron(curses.A_BOLD)
    stdscr.attron(curses.A_UNDERLINE)
    for char in title:
        title_string += char
        stdscr.addstr(start_y_title, start_x_title, title_string)
        time.sleep(random.random()*0.125)
        stdscr.refresh()
    stdscr.attroff(curses.color_pair(1))
    stdscr.attroff(curses.A_BOLD)
    stdscr.attroff(curses.A_UNDERLINE)

    subtitle_string = ''
    for char in subtitle:
        subtitle_string += char
        stdscr.addstr(start_y_subtitle, start_x_subtitle, subtitle_string)
        time.sleep(random.random()*0.125)
        stdscr.refresh()

    time.sleep(1.5)

    knapsack = ThiefsKnapsack(5, 5)
    answer = knapsack.optimize_booty(stdscr)

    stdscr.addstr(HEIGHT - 3, 1, f'Optimal Booty: {answer}')
    stdscr.addstr(HEIGHT - 2, 1, f'Press q to quit.')

    print(*knapsack.matrix, sep='\n')

    while k != ord('q'):
        k = stdscr.getch()


def main():
    curses.wrapper(greeting)


if __name__ == "__main__":
    main()




