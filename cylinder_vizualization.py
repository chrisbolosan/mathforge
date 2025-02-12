import pygame
import sympy as sp


pygame.init()

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

y = sp.Symbol('y')
weight_density = 9800 #force in weight
radius = 2
volume_element = (sp.pi *radius**2) * sp.Symbol('dy')
force = weight_density * volume_element
distance =y
work_integral = sp.integrate(force*distance, (y, 10, 12)) #bounds of integration
work_done = work_integral.simplify()

font = pygame.font.Font(None, 30)


running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.rect(screen, BLACK, (tank_x, tank_y, tank_width, tank_height), 2)
    #WATER
    pygame.draw.rect(screen, BLUE, (tank_x, tank_y + (tank_height - water_level), tank_width, water_level))

    #calculsations display
    work_text = font.render(f"Work Done: {work_done} N-m", True, BLACK)
    screen.blit(work_text, (50, 50))


    if water_level < max_water_height:
        water_level += filling_speed
    
    pygame.display.flip()
    pygame.time.delay(100)


pygame.quit()