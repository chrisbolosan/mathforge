import pygame
import sympy as sp

WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vizualization of Cyclinder Water Pump work")

WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

tank_x, tank_y = 250, 100
tank_width, tank_height = 100,200
water_level = 0

#some water physics here
max_water_height = tank_height //2
filling_speed = 1

pygame.init()

