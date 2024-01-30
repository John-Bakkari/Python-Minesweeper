"""
COMP.CS.100 Ohjelmointi 1 / Programming 1

Project 4: Minesweeper

Minesweeper game where you can choose the amount of rows and columns for the
game board size and the number of mines in it. The location of mines are
generated randomly and left-clicking on an empty cell, reveals clues about
nearby mines. Cells can be tagged with color orange when right-clicking.
The game is won by revealing all cells except the ones with the mines. If a
mine is left-clicked, the game ends. When the game is ended, all the mines are
revealed. Only one game can be generated at a time. The program ends when the
QUIT-button is pressed in the MAIN-window.
"""

import tkinter as tk
import ctypes
import sys
import random
import time


class settingsinterface:
    """
    Class for the game settings.
    """

    def __init__(self):
        """
        Function for the main window.
        """
        # Main window.
        self.main_window = tk.Tk()
        self.main_window.title('Minesweeper settings')

        # Entry for the wanted amount of rows in the game board.
        self.rows = tk.Entry(self.main_window)
        self.rows_label = tk.Label(self.main_window, text='ROWS: ')
        self.rows.grid(row=0, column=1, sticky=tk.E)
        self.rows_label.grid(row=0, column=0)

        # Entry for the wanted amount of columns in the game board.
        self.columns = tk.Entry(self.main_window)
        self.columns_label = tk.Label(self.main_window, text='COLUMNS: ')
        self.columns.grid(row=1, column=1, sticky=tk.E)
        self.columns_label.grid(row=1, column=0)

        # Entry for the wanted amount of mines in the game board.
        self.mines = tk.Entry(self.main_window)
        self.mines_label = tk.Label(self.main_window, text='MINES: ')
        self.mines.grid(row=2, column=1, sticky=tk.E)
        self.mines_label.grid(row=2, column=0)

        # Empty space for better visuals in the main window.
        self.empty = tk.Entry(self.main_window)
        self.empty_label = tk.Label(self.main_window, text='                ')
        self.empty_label.grid(row=3, column=2)

        # Quit button.
        self.__stop_button = tk.Button(self.main_window, text='QUIT', command=self.stop,
                                    borderwidth=2, relief=tk.GROOVE)
        self.__stop_button.grid(row=5, column=1)

        # Generate the game board.
        self.__generate_grid_button = tk.Button(self.main_window, text='GENERATE GAMEGRID', command=self.generate_grid,
                                                borderwidth=2, relief=tk.GROOVE)
        self.__generate_grid_button.grid(row=4, column=1)

    def get_rows_content(self):
        """
        Function that returns the amount of rows wanted and checks if the input is a number.

        :return: int, number of the wanted rows.
        """
        amount_of_rows = self.rows.get()
        if (amount_of_rows.isdigit() == False):
            return 0
        else:
            return int(amount_of_rows)

    def get_columns_content(self):
        """
        Function that returns the amount of columns wanted and checks if the input is a number.

        :return: int, number of the wanted columns.
        """
        amount_of_columns = self.columns.get()
        if (amount_of_columns.isdigit() == False):
            return 0
        else:
            return int(amount_of_columns)

    def get_mines_content(self):
        """
        Function that returns the amount of mines wanted and checks if the input is a number.

        :return: int, number of the wanted mines.
        """
        amount_of_mines = self.mines.get()
        if (amount_of_mines.isdigit() == False):
            return 0
        else:
            return int(amount_of_mines)


    def stop(self):
        """
        Ends the execution of the program.
        """
        self.main_window.destroy()
        sys.exit()

    def start(self):
        """
        Starts the mainloop.
        """
        self.main_window.mainloop()

    def generate_grid(self):
        """
        Generates the GAMEGRID-window.
        """
        # Checks if there is already existing game ongoing.
        if Cell.all != []:
            ctypes.windll.user32.MessageBoxW(0,'ONLY ONE GAME CAN BE PLAYED AT A TIME','ERROR:', 0)
            return

        # Gets the wanted number of rows and checks if the number is acceptable.
        R = self.get_rows_content()
        if R < 1:
            ctypes.windll.user32.MessageBoxW(0, 'NUMBER OF ROWS CAN NOT BE LESS THAN 1' ,'ERROR:', 0)
            return
        elif R > 15:
            ctypes.windll.user32.MessageBoxW(0, 'NUMBER OF ROWS CAN NOT BE MORE THAN 15' ,'ERROR:', 0)
            return

        # Gets the wanted number of columns and checks if the number is acceptable.
        C = self.get_columns_content()
        if C < 1:
            ctypes.windll.user32.MessageBoxW(0, 'NUMBER OF COLUMNS CAN NOT BE LESS THAN 1' ,'ERROR:', 0)
            return
        elif C > 15:
            ctypes.windll.user32.MessageBoxW(0, 'NUMBER OF COLUMNS CAN NOT BE MORE THAN 15' ,'ERROR:', 0)
            return

        # Gets the wanted number of mines and checks if the number is acceptable.
        M = self.get_mines_content()
        if M < 1:
            ctypes.windll.user32.MessageBoxW(0, 'NUMBER OF MINES CAN NOT BE LESS THAN 1' ,'ERROR:', 0)
            return
        elif M >= R*C:
            ctypes.windll.user32.MessageBoxW(0, 'NUMBER OF MINES CAN NOT BE EQUAL OR MORE THAN THE NUMBER OF CELLS' ,'ERROR:', 0)
            return

        # Creates the GAMEGRID-window.
        self.gamegrid = tk.Tk()
        self.gamegrid.title('GAMEGRID')
        self.gamegrid.geometry(f'{650}x{550}')

        # Top frame of the gamegrid-window.
        top_frame = tk.Frame(self.gamegrid, bg='#ffcc99', width=700, height=140)
        top_frame.place(x=0, y=0)

        # Left frame of the gamegrid-window.
        left_frame = tk.Frame(self.gamegrid, bg='#ffcc99', width=3000, height=560)
        left_frame.place(x=0, y=25)

        # Center frame of the gamegrid-window.
        center_frame = tk.Frame(self.gamegrid, bg='#ffcc99', width=500, height=560)
        center_frame.place(x=100, y=100)

        # Exit button to close the GAMEGRID-window.
        self.__stop_button = tk.Button(top_frame, text='EXIT', command=self.end,
                                       borderwidth=2, relief=tk.GROOVE)
        self.__stop_button.grid(row=0, column=2)

        # Generates the wanted amount of cells for the GAMEGRID.
        for x in range(R):
            for y in range(C):
                c = Cell(x, y)
                c.create_btn(center_frame)
                c.cell_btn.grid(column=x, row=y)

        # Counters for the cells left and overall mines in the GAMEGRID.
        Cell.set_cell_count(left_frame, R, C)
        Cell.create_cell_count(left_frame)
        Cell.cell_count_label_obj.place(x=50, y=-10)
        Cell.set_mine_amount(left_frame, M)
        Cell.create_mine_count(left_frame)
        Cell.mine_amount_label_obj.place(x=400, y=-10)

        # Randomizes the mines.
        Cell.randomize_mines()

    def end(self):
        """
        Function to close the GAMEGRID-window.
        """
        Cell.clear_mine_field(self)
        self.gamegrid.destroy()


class Cell:
    """
    Class for the generated cells.
    """
    all = []
    cell_count_label_obj = None
    cell_count = 0
    amount_of_mines = 0

    def __init__(self, x, y, is_mine=False):
        # Cell attributes.
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_cell = False
        self.cell_btn = None
        self.x = x
        self.y = y

        # Appends the objects to the Cell.all list to store the instances of the Cell class.
        Cell.all.append(self)

    def create_btn(self, location):
        """
        Function for creating a button for the cell.

        :param location: Frame, location for the cells in the GAMEGRID-window.
        """
        btn = tk.Button(location, width=3, height=1)
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn = btn

    def set_cell_count(self,rows, columns):
        """
        Function to store the number of the cells in the GAMEGRID.

        :param rows: int, number of the rows.
        :param columns: int, number of the columns.
        """
        Cell.cell_count = rows * columns

    @staticmethod
    def create_cell_count(location):
        """
        Function to create a counter for the remaining cells unopened in the GAMEGRID.

        :param location: Frame, location of the cell counter in the GAMEGRID.
        """
        label = tk.Label(
            location,
            bg='#ffcc99',
            text=f"CELLS LEFT = {Cell.cell_count}",
            width=18,
            height=3,
            font=("", 18)
        )
        Cell.cell_count_label_obj = label

    def create_mine_count(location):
        """
        Function to create a counter for the number of mines in the GAMEGRID.

        :param location: Frame, location of the mine counter in the GAMEGRID.
        """
        label = tk.Label(
            location,
            bg='#ffcc99',
            text=f"MINES = {Cell.amount_of_mines}",
            width=12,
            height=3,
            font=("", 18)
        )
        Cell.mine_amount_label_obj = label

    def left_click_actions(self, event):
        """
        Function for left-clicking on a cell.

        :param event:
        """
        # If left-clicked cell is a mine.
        if self.is_mine:
            self.show_mine()

        else:
            # Reveal the number of nearby mines.
            if self.mines_len == 0:
                for obj in self.surround_cells:
                    obj.show_cell()
            self.show_cell()

            # If the remaining cells are mines, VICTORY!
            if Cell.cell_count == self.amount_of_mines:
                ctypes.windll.user32.MessageBoxW(0, 'CONGRATULATIONS! YOU WON!', 'GAME OVER', 0)

                # Disables all the buttons of the cells and reveals the location of all the mines.
                for cell in Cell.all:
                    cell.cell_btn.unbind('<Button-1>')
                    cell.cell_btn.unbind('<Button-3>')
                    if cell.is_mine:
                        cell.cell_btn.configure(bg='red')
                    else:
                        cell.cell_btn.configure(bg='green')

        # Disables the pressed button of the cell.
        self.cell_btn.unbind('<Button-1>')
        self.cell_btn.unbind('<Button-3>')

    def get_cell_by_axis(self, x, y):
        """
        Function to return the wanted cell by location.

        :param x: Int, x-axis cell location number.
        :param y: Int, y-axis cell location number.
        :return cell: Object, searched cell.
        """
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surround_cells(self):
        """
        Function to gather all the surrounding cells of a left-clicked cell and
        return them in a list.

        :return surrounding_cells: List, all the surrounding cells.
        """
        # Gathers all the surrounding cells in a list.
        surrounding_cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]
        surrounding_cells = [cell for cell in surrounding_cells if cell is not None]

        # Returns the list of surrounding cells.
        return surrounding_cells

    def show_cell(self):
        """
        Function to open the left-clicked cell.
        """
        # If cell is not opened yet, opens it.
        if not self.is_opened:
            # Reduces the number of cells left and shows the amount of mines nearby.
            Cell.cell_count -= 1
            self.cell_btn.configure(text=self.mines_len)

            # Updates the cell_count label.
            if Cell.cell_count_label_obj:
                Cell.cell_count_label_obj.configure(
                    text=f"CELLS LEFT = {Cell.cell_count}"
                )
            self.cell_btn.configure(bg='SystemButtonFace')

        # Cell is opened.
        self.is_opened = True

    @property
    def mines_len(self):
        """
        Function to return the number of mines surrounding the given cell.

        :return i: Int, number of mines nearby.
        """
        i = 0
        for cell in self.surround_cells:
            if cell.is_mine:
                i += 1
        return i

    def show_mine(self):
        """
        Function to reveal the cell as a mine and end the game.
        """
        # Colours the cell red and gives the game over message.
        self.cell_btn.configure(bg='red')
        ctypes.windll.user32.MessageBoxW(0, 'YOU CLICKED ON A MINE', 'GAME OVER', 0)

        # Disables all the cell buttons and reveals all the mines.
        for cell in Cell.all:
            cell.cell_btn.unbind('<Button-1>')
            cell.cell_btn.unbind('<Button-3>')
            if cell.is_mine:
                cell.cell_btn.configure(bg='red')

    def right_click_actions(self, event):
        """
        Function to mark cells with color orange when right-clicked.

        :param event:
        """
        # Marks the cell if possible.
        if not self.is_mine_cell:
            self.cell_btn.configure(bg='orange')
            self.is_mine_cell = True

        # Takes the mark away.
        else:
            self.cell_btn.configure(bg='SystemButtonFace')
            self.is_mine_cell = False

    def set_mine_amount(self, mines):
        """
        Function to store the number of all the mines in the game board.

        :param mines: Int, number of all the mines in the game board.
        """
        Cell.amount_of_mines = mines

    @staticmethod
    def randomize_mines():
        """
        Function to randomize the mines.
        """
        # Gathers a list of wanted amount of randomly chosen cells to be made into mines.
        picked_as_mines = random.sample(Cell.all, Cell.amount_of_mines)

        # All the gathered cells are made into mines.
        for picked_mine in picked_as_mines:
            picked_mine.is_mine = True

    def clear_mine_field(self):
        """
        Function to reset the game when the GAMEGRID is closed.
        """
        for cell in Cell.all:
            self.is_opened = False
            self.is_mine_cell = False
            self.cell_btn = None

        Cell.all.clear()
        Cell.cell_count = 0
        Cell.amount_of_mines = 0

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"


def main():
    """
    Starts the program.
    """
    ui = settingsinterface()
    ui.start()

if __name__ == "__main__":
    main()