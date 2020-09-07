import tkinter as tk
from button import *
from SudokuGrid import *
from tkinter import messagebox


# Class which gets instantiated to run the application
class App:
    root = tk.Tk()
    root.withdraw()

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sudoku Solver")
        self.__window__ = pygame.display.set_mode((WIDTH, HEIGHT))
        self.__sudoku__ = SudokuGrid()
        self.__appRunning__ = True
        self.__mousePosition__ = None
        self.__buttons__ = []
        self.__load__()

    def run(self):
        while self.__appRunning__:
            self.__events__()
            self.__update__()
            self.__draw__()

        pygame.quit()
        sys.exit()

    def __events__(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__appRunning__ = False

            # Mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.__mouseOverGrid__()

                if not self.__sudoku__.gridSolved() and not self.__sudoku__.isRunning():
                    if selected:
                        self.__sudoku__.highlightElement(selected)

                for button in self.__buttons__:
                    if button.highlighted:
                        button.press()

            # Keyboard input
            if not self.__sudoku__.gridSolved():
                if event.type == pygame.KEYDOWN:
                    if self.__sudoku__.checkHighlighted() and self.__checkInt__(event.unicode):
                        self.__sudoku__.allocateValue(int(event.unicode))

    def __update__(self):
        self.__mousePosition__ = pygame.mouse.get_pos()

        # Update each button - using mousePos
        for button in self.__buttons__:
            button.update(self.__mousePosition__)

    def __draw__(self):
        self.__window__.fill(WHITE)

        # Draw all buttons within the window
        for button in self.__buttons__:
            button.draw(self.__window__)

        self.__sudoku__.draw(self.__window__)
        pygame.display.update()

    def __loadButtons__(self):
        self.__buttons__.append(Button(150, 40, WIDTH // 5, 40, "Solve", function=self.__sudoku__.startSolve))
        self.__buttons__.append(Button(350, 40, WIDTH // 5, 40, "Reset Board", function=self.__sudoku__.resetBoard))

    def __load__(self):
        self.__loadButtons__()

    def __mouseOverGrid__(self):
        if self.__mousePosition__[0] < gridPosition[0] or self.__mousePosition__[1] < gridPosition[1]:
            return False
        if self.__mousePosition__[0] > gridPosition[0] + GRID_SIZE or self.__mousePosition__[1] > gridPosition[
            1] + GRID_SIZE:
            return False

        return (self.__mousePosition__[0] - gridPosition[0]) // CELL_SIZE, (
                    self.__mousePosition__[1] - gridPosition[1]) // CELL_SIZE

    # Checks to check input is a number
    def __checkInt__(self, string):
        try:
            int(string)
            return True
        except:
            return False

    @staticmethod
    def popupBox(title, message):
        messagebox.showinfo(title, message)