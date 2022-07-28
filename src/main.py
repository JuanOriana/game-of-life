from cProfile import run
from cgitb import small
from pickle import STOP
import pygame
import sys
import math
import random

from src import grid as gr, button as btn, slider as sdr

pygame.init()
pygame.display.set_caption("Conway's Game of Life")
size = width, height = 1000, 700
grid_size = grid_width, grid_height = 900, 550
x_offset = (width - grid_width) // 2
y_offset = 80

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


def draw_buttons():
    for button in buttons:
        button.draw(screen)



button_size = button_width, button_height = 80, 30
button_run = btn.Button(820, 30, button_width, button_height, GREEN, smallFont.render('Run!', True, BLACK))
button_stop = btn.Button(820, 30, button_width, button_height, RED, smallFont.render('Stop!', True, BLACK))

button_calculate = button_run
button_clear = btn.Button(850, 650, button_width, button_height, WHITE, smallFont.render("Clear", True, BLACK))
button_random = btn.Button(760, 650, button_width, button_height, ORANGE, smallFont.render("Random!", True, WHITE))

button_add = btn.Button(80, 650, button_width, button_height, BLUE, smallFont.render("Block", True, WHITE))
button_erase = btn.Button(170, 650, button_width, button_height, BLUE, smallFont.render("Erase", True, WHITE))

buttons = [button_calculate,button_clear,button_random,button_add,button_erase]
button_add.toggle()
draw_buttons()

slider_label = smallFont.render("Speed", True, WHITE)
zero_label = smallFont.render("0", True, WHITE)
hundred_label = smallFont.render("100", True, WHITE)

slider = sdr.Slider(130,45,150,5)
slider.draw(screen)
screen.blit(slider_label,(180,20))
screen.blit(zero_label,(105,37))
screen.blit(hundred_label,(290,37))


stateLabel = smallFont.render("Current state :", True, WHITE)
screen.blit(stateLabel, (650, 35))
stoppedLabel = smallFont.render("stopped", True, RED)
startedLabel = smallFont.render("started", True, GREEN)
screen.blit(stoppedLabel, (750, 35))

def correct_label(running):
    if running: return startedLabel
    return stoppedLabel

def correct_button(running):
    if running: return button_stop
    return button_run


def draw_grid(grid):
    for i in range(X_CELL):
        for j in range(Y_CELL):
            cell = grid.get_cell(i, j)
            cell_color = WHITE if cell else BLACK
            pygame.draw.rect(screen, cell_color, (x_offset + i * CELL_SIZE, y_offset + j * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, WHITE, (x_offset + i * CELL_SIZE, y_offset + j * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                             width=1)
frame = 0
running = False
block_type = gr.ALIVE

while True:
    rate = (100-slider.get_volume()+30)//5
    frame = (frame+1)%(rate)
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
                grid.randomize(0.1)
            if button_add.collides(mouse):
                block_type = gr.ALIVE
                button_add.toggle()
                button_erase.untoggle()
                button_add.draw(screen)
                button_erase.draw(screen)
            if button_erase.collides(mouse):
                block_type = gr.DEAD
                button_erase.toggle()
                button_add.untoggle()
                button_add.draw(screen)
                button_erase.draw(screen)
            if button_calculate.collides(mouse):
                running = not running
                pygame.draw.rect(screen, BLACK, (750, 35, 70, 50))
                screen.blit(correct_label(running), (750, 35))
                button_calculate = correct_button(running)
                button_calculate.draw(screen)




    # Not using event.get() allows for dragging
    click, _, _ = pygame.mouse.get_pressed()
    if click == 1:
        mouse = pygame.mouse.get_pos()
        if slider.on_slider(mouse[0],mouse[1]):
            slider.handle_event(screen,mouse[0])
        if x_offset <= mouse[0] <= width - x_offset and y_offset <= mouse[1] <= y_offset + grid_height:
            cell_x = (mouse[0] - x_offset) // CELL_SIZE
            cell_y = (mouse[1] - y_offset) // CELL_SIZE
            grid.set_cell(cell_x, cell_y, block_type)

    draw_grid(grid)
    pygame.display.flip()