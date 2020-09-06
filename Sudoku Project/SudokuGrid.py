import pygame, sys
import threading
import copy
import App
from settings import *


# Used to store all back-end work relating to the Sudoku board
# (Drawing board, solving functions)
class SudokuGrid:
    def __init__(self):
        self.__grid__ = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     ]
        self.answerBoard = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            ]
        self.lockedNodes = []
        self.selected = None
        self.complete = False
        self.font = pygame.font.SysFont("Ariel", 24)
        self.answerThread = None

    def draw(self, window):
        # Draw user selected area
        if self.selected:
            self.drawSelection(window, self.selected)

        self.fillLockedNodes(window, self.lockedNodes)

        if not self.complete:
            self.allocateNumbers(window, self.__grid__)
        else:
            self.allocateNumbers(window, self.answerBoard)

        self.drawGrid(window)

    # Highlight corresponding grid square
    def drawSelection(self, window, position):
        pygame.draw.rect(window, LIGHTBLUE, ((position[0] * CELL_SIZE) + gridPosition[0],
                                             (position[1] * CELL_SIZE) + gridPosition[1], CELL_SIZE, CELL_SIZE))

    # Allocate numbers from array onto the GUI board
    def allocateNumbers(self, window, grid):
        for yind, row in enumerate(grid):
            for xind, col in enumerate(row):
                if col != 0:
                    position = [xind * CELL_SIZE + gridPosition[0], yind * CELL_SIZE + gridPosition[1]]
                    self.addingText(window, str(col), position)

    # Add text to designated screen area on game board
    def addingText(self, window, numberValue, position, colour=BLACK):
        font = self.font.render(numberValue, False, colour)

        width = font.get_width()
        height = font.get_height()

        position[0] += (CELL_SIZE - width) / 2
        position[1] += (CELL_SIZE - height) / 2

        window.blit(font, position)

    def drawGrid(self, window):
        pygame.draw.rect(window, BLACK, (gridPosition[0], gridPosition[1], WIDTH - 150, HEIGHT - 150), 2)

        for x in range(9):
            # Changing thickness depending on line number
            if x % 3 != 0:
                # Vertical Lines
                pygame.draw.line(window, BLACK, (gridPosition[0] + (x * CELL_SIZE), gridPosition[1]),
                                 (gridPosition[0] + (x * CELL_SIZE), gridPosition[1] + 450))
                # Horizontal Lines
                pygame.draw.line(window, BLACK, (gridPosition[0], gridPosition[1] + (x * CELL_SIZE)),
                                 (gridPosition[0] + 450, gridPosition[1] + + (x * CELL_SIZE)))
            else:
                # Vertical Lines
                pygame.draw.line(window, BLACK, (gridPosition[0] + (x * CELL_SIZE), gridPosition[1]),
                                 (gridPosition[0] + (x * CELL_SIZE), gridPosition[1] + 450), 2)
                # Horizontal Lines
                pygame.draw.line(window, BLACK, (gridPosition[0], gridPosition[1] + (x * CELL_SIZE)),
                                 (gridPosition[0] + 450, gridPosition[1] + + (x * CELL_SIZE)), 2)

    # Colour default sudoku numbers
    def fillLockedNodes(self, window, lockedNodes):
        for lockedNode in lockedNodes:
            pygame.draw.rect(window, LOCKED_COLOUR, (lockedNode[0] * CELL_SIZE + gridPosition[0],
                                                     lockedNode[1] * CELL_SIZE + gridPosition[1], CELL_SIZE,
                                                     CELL_SIZE))

    # Appending what nodes to be 'locked' in lockedNodes list
    def setLockedElements(self):
        for yIndex, row in enumerate(self.__grid__):
            for xIndex, num in enumerate(row):
                if num != 0:
                    self.lockedNodes.append([xIndex, yIndex])

    def highlightElement(self, coord):
        self.selected = coord

    def checkHighlighted(self):
        if self.selected is not None:
            return True
        else:
            return False

    # Allocates number to sudoku square, using 'selected' position
    def allocateValue(self, value):
        self.__grid__[self.selected[1]][self.selected[0]] = value

    # Function called from 'Solve' button in app.
    # Tkinter is not thread safe - popupBox() needs to be called on same thread as window,
    # so the thread is started after.
    def startSolve(self):
        if not self.complete:
            self.setLockedElements()
            if len(self.lockedNodes) < 17:
                App.App.popupBox("Error", "Less than 17 positions have been filled.")
            elif not self.__validGrid__(self.__grid__):
                App.App.popupBox("Error", "Invalid number has been placed within the grid.")
            else:
                self.startThread()

    # Can't call 'sudokuSolver' directly from thread as it's recursive.
    def solve(self):
        self.__sudokuSolver__(self.__grid__)

    # The core backtracking algorithm to solve the puzzle.
    def __sudokuSolver__(self, grid):
        if self.__validGrid__(grid):
            for row in range(9):
                for col in range(9):
                    if grid[row][col] == 0:
                        for n in range(1, 10):
                            if self.__possibleMove__(grid, (row, col), n):
                                grid[row][col] = n
                                self.__sudokuSolver__(grid)
                                grid[row][col] = 0
                        return

            self.answerBoard = copy.deepcopy(grid)
            self.grid = self.answerBoard
            self.complete = True

    # Checks a specific position meets the Sudoku critera
    def __possibleMove__(self, grid, pos, n):
        # Check Row
        for i in range(0, 9):
            if grid[pos[0]][i] == n and i != pos[1]:
                return False
        # Check Col
        for i in range(0, 9):
            if grid[i][pos[1]] == n and i != pos[0]:
                return False

        x = (pos[1] // 3) * 3
        y = (pos[0] // 3) * 3

        # Cycle through 3x3 square
        for i in range(0, 3):
            for j in range(0, 3):
                if grid[y + i][x + j] == n and (y + i, x + j) != pos:
                    return False

        return True

    # Returns if all numbers entered meet the Sudoku critera
    def __validGrid__(self, grid):
        for row in range(9):
            for col in range(9):
                if grid[row][col] != 0:
                    if not self.__possibleMove__(grid, (row, col), grid[row][col]):
                        return False

        return True

    def resetBoard(self):
        for row in range(len(self.__grid__)):
            for col in range(len(self.__grid__)):
                self.__grid__[row][col] = 0

        self.selected = None
        self.lockedNodes.clear()
        self.complete = False

    def gridSolved(self):
        if self.complete:
            return True
        else:
            return False

    def startThread(self):
        self.answerThread = threading.Thread(target=self.solve)
        self.answerThread.start()