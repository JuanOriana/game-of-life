from cProfile import run
import pygame
import sys
import math
import random

from src import grid as gr, button as btn

pygame.init()
pygame.display.set_caption("Pathfinding Algorithm Visualization")
size = width, height = 1000, 800
grid_size = grid_width, grid_height = 800, 600
x_offset = (width - grid_width) // 2

# cell
CELL_SIZE = 20
X_CELL = grid_width // CELL_SIZE
Y_CELL = grid_height // CELL_SIZE
RAND_TOLERANCE = 0.3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (140, 140, 140)
ORANGE = (255, 100, 100)
RED = (255, 60, 30)
GREEN = (45, 255, 20)
BLUE = (90, 10, 255)
YELLOW = (210, 205, 10)
# Cell-color correspondence
colors = [BLACK, BLUE, ORANGE, GREEN, RED, YELLOW]

screen = pygame.display.set_mode(size)

smallFont = pygame.font.Font("../resources/OpenSans-Regular.ttf", 14)
mediumFont = pygame.font.Font("../resources/OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("../resources/OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("../resources/OpenSans-Regular.ttf", 60)

grid = gr.Grid(X_CELL, Y_CELL)

# Non changing graphics

# Background
screen.fill(BLACK)


# Title
# title = mediumFont.render("Algo-Vis", True, WHITE)
# titleRect = title.get_rect()
# titleRect.center = ((width / 2), 50)
# screen.blit(title, titleRect)


# Buttons
def untoggle_all(buttons):
    for button in buttons:
        button.untoggle()


def draw_buttons():
    for button in buttons:
        button.draw(screen)



button_size = button_width, button_height = 80, 30
button_calculate = btn.Button(820, 70, button_width, button_height, GREEN, smallFont.render('Calculate!', True, BLACK))
button_clear = btn.Button(820, 750, button_width, button_height, WHITE, smallFont.render("Clear", True, BLACK))
button_random = btn.Button(730, 750, button_width, button_height, BLUE, smallFont.render("Random!", True, WHITE))

button_block = btn.Button(280, 750, button_width, button_height, BLUE, smallFont.render("Block", True, WHITE))
button_erase = btn.Button(370, 750, button_width, button_height, GREY, smallFont.render("Erase", True, BLACK))

buttons = [button_calculate,button_clear,button_random,button_block,button_erase]
draw_buttons()



def draw_grid(grid):
    for i in range(X_CELL):
        for j in range(Y_CELL):
            cell = grid.get_cell(i, j)
            cell_color = WHITE if cell else BLACK
            # Paths change color as they get further from start
            pygame.draw.rect(screen, cell_color, (x_offset + i * CELL_SIZE, 125 + j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, WHITE, (x_offset + i * CELL_SIZE, 125 + j * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                             width=1)

    # # Analyzer flags
    # if analyzer.flag != algo.INACTIVE:
    #     # Erase old labels
    #     pygame.draw.rect(screen, BLACK, (0, 0, 600, 60))
    #     stateLabel = smallFont.render("Current state :", True, WHITE)
    #     screen.blit(stateLabel, (100, 20))
    #     if analyzer.flag == algo.ANALYZING:
    #         flagColor = ORANGE
    #         flagLabel = "Analyzing"
    #     elif analyzer.flag == algo.SUCCESS:
    #         countLabel = "Found path length: " + str(analyzer.pathLength)
    #         stateLabel = smallFont.render(countLabel, True, GREEN)
    #         screen.blit(stateLabel, (350, 30))
    #         flagColor = GREEN
    #         flagLabel = "Success!"
    #     else:
    #         flagColor = RED
    #         flagLabel = "Failed to find path"
    #     stateLabel = smallFont.render(flagLabel, True, flagColor)
    #     screen.blit(stateLabel, (200, 20))

    #     countLabel = "Visited nodes: " + str(analyzer.visitCount)
    #     stateLabel = smallFont.render(countLabel, True, WHITE)
    #     screen.blit(stateLabel, (100, 40))
running = False
frame = 0

while True:
    frame = (frame+1)%30
    if (frame == 0 and running):
        grid.evolve()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if button_clear.collides(mouse):
                grid.clear_state()
            if button_random.collides(mouse):
                grid.randomize(0.3)
            if button_calculate.collides(mouse):
                running = not running


    # Not using event.get() allows for dragging
    click, _, _ = pygame.mouse.get_pressed()
    if click == 1:
        mouse = pygame.mouse.get_pos()
        if x_offset <= mouse[0] <= width - x_offset and 125 <= mouse[1] <= 125 + grid_height:
            cell_x = (mouse[0] - x_offset) // CELL_SIZE
            cell_y = (mouse[1] - 125) // CELL_SIZE
            cell = gr.ALIVE
            for button in buttons:
                if button.pressed:
                    cell = ALIVE
            grid.set_cell(cell_x, cell_y, cell)
            # Add and remove in chunks of 4
            # if cell == mz.BLOCKED or cell == mz.EMPTY:
            #     maze.setCell(cellX + 1, cellY, cell)
            #     maze.setCell(cellX, cellY + 1, cell)
            #     maze.setCell(cellX + 1, cellY + 1, cell)

    draw_grid(grid)
    pygame.display.flip()