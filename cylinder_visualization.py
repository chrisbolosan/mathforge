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

TANK_X, TANK_Y = 250, 100
TANK_WIDTH, TANK_HEIGHT = 100,200
RESERVOIR_Y = 350
PIPE_WIDTH = 10
PIPE_X = TANK_X + TANK_WIDTH // 2 - PIPE_WIDTH // 2
PIPE_HEIGHT = TANK_Y - RESERVOIR_Y
PUMP_X, PUMP_Y = PIPE_X - 15, TANK_Y + TANK_HEIGHT  # Position of the pump


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

MAX_WATER_HEIGHT = TANK_HEIGHT //2
FILLING_SPEED = 1

y = sp.Symbol('y')
WEIGHT_DENSITY = 9800
RADIUS = 2
VOLUME_ELEMENT = (sp.pi *RADIUS**2) * sp.Symbol('dy')
FORCE = WEIGHT_DENSITY * VOLUME_ELEMENT
DISTANCE =y
WORK_INTEGRAL = sp.integrate(FORCE*DISTANCE, (y, 10, 12)) 
WORK_DONE = WORK_INTEGRAL.simplify()

st.title("Water Tank Work Calculation")
st.write("Simulating water filling in a tank.")

image_placeholder = st.empty()
    
if "water_particles" not in st.session_state:
    st.session_state.water_particles = []

def draw_ui(frame):
    screen.fill(WHITE)
    
    WAVE_AMPLITUDE = 8
    WAVE_FREQUENCY = 0.1
    RESERVOIR_WATER_LEVEL = RESERVOIR_Y + 30
    WAVE_POINTS = [
      (x, RESERVOIR_WATER_LEVEL + math.sin(x * WAVE_FREQUENCY + frame * 0.2) * WAVE_AMPLITUDE)
        for x in range(0, WIDTH, 5) 
    ]
    pygame.draw.polygon(screen, BLUE, [(0, HEIGHT), *WAVE_POINTS, (WIDTH, HEIGHT)])
    pygame.draw.rect(screen, GRAY, (PUMP_X, PUMP_Y, 40, 90))    
    pygame.draw.rect(screen, BLACK, (TANK_X, TANK_Y, TANK_WIDTH, TANK_HEIGHT), 2)
    pygame.draw.rect(screen, BLACK, (PIPE_X, TANK_Y + TANK_HEIGHT +30, PIPE_WIDTH, RESERVOIR_Y - TANK_Y - TANK_HEIGHT+10),2)
    pygame.draw.rect(screen, BLUE, (TANK_X, TANK_Y + (TANK_HEIGHT - st.session_state.water_level), TANK_WIDTH, st.session_state.water_level))

    if st.session_state.filling:
        st.session_state.water_particles.append([PIPE_X + PIPE_WIDTH // 2, RESERVOIR_Y])

    for particle in st.session_state.water_particles:
        particle[1] -= 6.5
        if particle[1] < PUMP_Y:
            st.session_state.water_particles.remove(particle)
        else:
            pygame.draw.circle(screen, BLUE, (particle[0], particle[1]), 3)

    FONT = pygame.font.Font(None, 30)
    WORK_TEXT = FONT.render(f"Work Done: {WORK_DONE} N-m", True, BLACK)
    screen.blit(WORK_TEXT, (50, 50))

    return screen

frame_count = 0

while st.session_state.filling and st.session_state.water_level < MAX_WATER_HEIGHT:
    st.session_state.water_level += FILLING_SPEED
    time.sleep(0.1)
    draw_ui(frame_count)
    
    frame_array = pygame.surfarray.array3d(screen)  
    frame_array = np.rot90(frame_array,-1) 
    frame_array = np.fliplr(frame_array)
    frame_image = Image.fromarray(frame_array) 
    image_placeholder.image( frame_image,caption="Water Tank Simulation", use_container_width=True)
    
    frame_count += 1 
    time.sleep(0.1)

if not st.session_state.filling or st.session_state.water_level >= MAX_WATER_HEIGHT:
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

