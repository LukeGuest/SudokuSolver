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
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.sudoku = SudokuGrid()
        self.running = True
        self.mousePosition = None
        self.buttons = []
        self.load()

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()

        pygame.quit()
        sys.exit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Mouse input
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOverGrid()

                if not self.sudoku.gridSolved():
                    if selected:
                        self.sudoku.highlightElement(selected)

                for button in self.buttons:
                    if button.highlighted:
                        button.press()

            # Keyboard input
            if not self.sudoku.gridSolved():
                if event.type == pygame.KEYDOWN:
                    if self.sudoku.checkHighlighted() and self.checkInt(event.unicode):
                        self.sudoku.allocateValue(int(event.unicode))

    def update(self):
        self.mousePosition = pygame.mouse.get_pos()

        # Update each button - using mousePos
        for button in self.buttons:
            button.update(self.mousePosition)

    def draw(self):
        self.window.fill(WHITE)

        # Draw all buttons within the window
        for button in self.buttons:
            button.draw(self.window)

        self.sudoku.draw(self.window)
        pygame.display.update()

    def loadButtons(self):
        self.buttons.append(Button(150, 40, WIDTH // 5, 40, "Solve", function=self.sudoku.startSolve))
        self.buttons.append(Button(350, 40, WIDTH // 5, 40, "Reset Board", function=self.sudoku.resetBoard))

    def load(self):
        self.loadButtons()

    def mouseOverGrid(self):
        if self.mousePosition[0] < gridPosition[0] or self.mousePosition[1] < gridPosition[1]:
            return False
        if self.mousePosition[0] > gridPosition[0] + GRID_SIZE or self.mousePosition[1] > gridPosition[
            1] + GRID_SIZE:
            return False

        return (self.mousePosition[0] - gridPosition[0]) // CELL_SIZE, (
                    self.mousePosition[1] - gridPosition[1]) // CELL_SIZE

    # Checks to check input is a number
    def checkInt(self, string):
        try:
            int(string)
            return True
        except:
            return False

    @staticmethod
    def popupBox(title, message):
        messagebox.showinfo(title, message)