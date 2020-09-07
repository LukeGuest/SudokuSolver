import pygame


# Class to create button objects
class Button:
    def __init__(self, xPosition, yPosition, width, height, text=None, colour=(172,172,172),
                 highlightedColour = (216,216,216), function = None, args=None):
        self.image = pygame.Surface((width, height))
        self.position = (xPosition, yPosition)
        self.width = width
        self.height = height
        self.rectangle = self.image.get_rect()
        self.rectangle.topleft = self.position
        self.text = text
        self.colour = colour
        self.highlightedColour = highlightedColour
        self.function = function
        self.args = args
        self.highlighted = False

    def update(self, mouse):
        if self.rectangle.collidepoint(mouse):
            self.highlighted = True
        else:
            self.highlighted = False

    def draw(self, window):
        # Change colour of button depending on being highlighted
        if self.highlighted:
            self.image.fill(self.highlightedColour)
        else:
            self.image.fill(self.colour)

        if self.text is not None:
            self.displayText(self.text)

        window.blit(self.image, self.position)

    def press(self):
        if self.args is not None:
            self.function(self.args)
        else:
            self.function()

    def displayText(self, text):
        font = pygame.font.SysFont("arial", 20, 1)
        text = font.render(text, False, (0, 0, 0))

        # Returns a tuple with the width and height
        textWidth, textHeight = text.get_size()

        # Floor division used to usew int
        x = (self.width - textWidth)//2
        y = (self.height - textHeight)//2

        self.image.blit(text, (x,y))
