import pygame
import sympy as sp
import streamlit as st
import numpy as np
from PIL import Image
import time
import math

pygame.init()

WIDTH, HEIGHT = 600, 500
screen = pygame.Surface((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

tank_x, tank_y = 250, 100
tank_width, tank_height = 100,200
reservoir_y = 350
pipe_width = 10
pipe_x = tank_x + tank_width // 2 - pipe_width // 2
pipe_height = tank_y - reservoir_y
pump_x, pump_y = pipe_x - 15, tank_y + tank_height  # Position of the pump


if "water_level" not in st.session_state:
    st.session_state.water_level = 0

if "filling" not in st.session_state:
    st.session_state.filling = False
    
if st.button("Start Pumping"):
    st.session_state.filling = True

if st.button("Stop Pumping"):
    st.session_state.filling = False
    
else:
    reset_pump_button = st.button("Reset Tank")
    if reset_pump_button:
        st.session_state.water_level = 0
        st.session_state.filling = True

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

st.title("Water Tank Work Calculation")
st.write("Simulating water filling in a tank.")

image_placeholder = st.empty()
    
if "water_particles" not in st.session_state:
    st.session_state.water_particles = []

def draw_ui(frame):
    screen.fill(WHITE)
    
    # Simulated wavy water surface in the reservoir
    wave_amplitude = 8
    wave_frequency = 0.1
    reservoir_water_level = reservoir_y + 30
    wave_points = [
      (x, reservoir_water_level + math.sin(x * wave_frequency + frame * 0.2) * wave_amplitude)
        for x in range(0, WIDTH, 5)  # **Cover full width with smaller gaps**
    ]
    pygame.draw.polygon(screen, BLUE, [(0, HEIGHT), *wave_points, (WIDTH, HEIGHT)])


    
    pygame.draw.rect(screen, GRAY, (pump_x, pump_y, 40, 90))
    
    # pygame.draw.rect(screen, BLUE, (0, reservoir_y, WIDTH, HEIGHT - reservoir_y))
    
    pygame.draw.rect(screen, BLACK, (tank_x, tank_y, tank_width, tank_height), 2)

    pygame.draw.rect(screen, BLACK, (pipe_x, tank_y + tank_height +30, pipe_width, reservoir_y - tank_y - tank_height+10),2)

    pygame.draw.rect(screen, BLUE, (tank_x, tank_y + (tank_height - st.session_state.water_level), tank_width, st.session_state.water_level))

    if st.session_state.filling:
        st.session_state.water_particles.append([pipe_x + pipe_width // 2, reservoir_y])

    for particle in st.session_state.water_particles:
        particle[1] -= 6.5
        if particle[1] < pump_y:
            st.session_state.water_particles.remove(particle)
        else:
            pygame.draw.circle(screen, BLUE, (particle[0], particle[1]), 3)

    font = pygame.font.Font(None, 30)
    work_text = font.render(f"Work Done: {work_done} N-m", True, BLACK)
    screen.blit(work_text, (50, 50))

    return screen

frame_count = 0
while st.session_state.filling and st.session_state.water_level < max_water_height:
    st.session_state.water_level += filling_speed
    time.sleep(0.1)
    draw_ui(frame_count)
    
    frame_array = pygame.surfarray.array3d(screen)  
    frame_array = np.rot90(frame_array,-1) 
    frame_array = np.fliplr(frame_array)
    frame_image = Image.fromarray(frame_array) 
    image_placeholder.image( frame_image,caption="Water Tank Simulation", use_container_width=True)
    
    frame_count += 1 
    time.sleep(0.1)

if not st.session_state.filling or st.session_state.water_level >= max_water_height:
    draw_ui(frame_count)
    frame_array = pygame.surfarray.array3d(screen)  
    frame_array = np.rot90(frame_array,-1) 
    frame_array = np.fliplr(frame_array)
    frame_image = Image.fromarray(frame_array) 
    image_placeholder.image( frame_image,caption="Water Tank Simulation", use_container_width=True)

draw_ui(frame_count)
frame_array = pygame.surfarray.array3d(screen)  
frame_array = np.rot90(frame_array,-1) 
frame_array = np.fliplr(frame_array)
frame_image = Image.fromarray(frame_array) 
image_placeholder.image( frame_image,caption="Water Tank Simulation", use_container_width=True)

