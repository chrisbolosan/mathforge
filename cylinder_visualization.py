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
LIGHT_BLUE = (135, 206, 235)
DARK_BLUE = (0, 0, 139)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
SILVER = (192, 192, 192)

TANK_X, TANK_Y = 250, 100
TANK_WIDTH, TANK_HEIGHT = 100, 200
RESERVOIR_Y = 350
PIPE_WIDTH = 20
PIPE_X = TANK_X + TANK_WIDTH // 2 - PIPE_WIDTH // 2
PIPE_HEIGHT = RESERVOIR_Y - (TANK_Y + TANK_HEIGHT)
PIPE_EXTENSION = 40  
PUMP_X = PIPE_X - 10
PUMP_Y = RESERVOIR_Y+10  

if "water_level" not in st.session_state:
    st.session_state.water_level = 0

if "filling" not in st.session_state:
    st.session_state.filling = False

if "water_particles" not in st.session_state:
    st.session_state.water_particles = []

image_placeholder = st.empty()

if st.button("Start Pumping"):
    st.session_state.filling = True

if st.button("Stop Pumping"):
    st.session_state.filling = False
    
else:
    reset_pump_button = st.button("Reset Tank")
    if reset_pump_button:
        st.session_state.water_level = 0
        st.session_state.filling = True

MAX_WATER_HEIGHT = TANK_HEIGHT  
FILLING_SPEED = 1

st.sidebar.title("Simulation Controls")
MAX_FILL_LEVEL = st.sidebar.slider("Maximum Fill Level", 0, 100, 100, 1)  # New control
ACTUAL_MAX_HEIGHT = (MAX_FILL_LEVEL / 100) * TANK_HEIGHT
FILLING_SPEED = st.sidebar.slider("Pump Speed", 0.5, 3.0, 1.0, 0.1)
WAVE_SPEED = st.sidebar.slider("Wave Speed", 0.1, 1.0, 0.2, 0.1)
PARTICLE_SPEED = st.sidebar.slider("Water Flow Speed", 3.0, 10.0, 6.5, 0.5)
WATER_COLOR = st.sidebar.color_picker("Water Color", "#0064FF")

WATER_COLOR_RGB = tuple(int(WATER_COLOR.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

def create_water_gradient(height, color):
    gradient = []
    base_color = list(color)
    for i in range(height):
        alpha = i / height
        lighter_color = [min(255, c + (255 - c) * (1 - alpha) * 0.3) for c in base_color]
        gradient.append(lighter_color)
    return gradient

def calculate_work(height):
    """Calculate work done to fill tank to current height"""
    if height <= 0:
        return 0
    
    WEIGHT_DENSITY = 9800  # n/m^3
    RADIUS = 2  # meters
    AREA = 3.14159 * RADIUS**2
    # clculation from bottom of tank to top of tank
    y1, y2 = 0, height / 100  
    return WEIGHT_DENSITY * AREA * (y2**2 - y1**2) / 2

def draw_ui(frame):
    screen.fill(WHITE)
    
    WAVE_AMPLITUDE = 8
    WAVE_FREQUENCY = 0.1
    RESERVOIR_WATER_LEVEL = RESERVOIR_Y + 30
    WAVE_POINTS = [
        (x, RESERVOIR_WATER_LEVEL + math.sin(x * WAVE_FREQUENCY + frame * WAVE_SPEED) * WAVE_AMPLITUDE)
        for x in range(0, WIDTH, 5)
    ]
    pygame.draw.polygon(screen, WATER_COLOR_RGB, [(0, HEIGHT), *WAVE_POINTS, (WIDTH, HEIGHT)])
    
    if st.session_state.filling:
        for x_offset in range(6):
            x_pos = PIPE_X + (PIPE_WIDTH * (x_offset + 1)) // 7

            pygame.draw.line(screen, WATER_COLOR_RGB,
                           (x_pos, PUMP_Y),
                           (x_pos, TANK_Y + TANK_HEIGHT - st.session_state.water_level),
                           2)

            pygame.draw.line(screen, WATER_COLOR_RGB,
                           (x_pos, RESERVOIR_Y + PIPE_EXTENSION),
                           (x_pos, PUMP_Y + 30),
                           2)
    
    pygame.draw.rect(screen, SILVER, (PIPE_X, TANK_Y + TANK_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT + PIPE_EXTENSION))
    pygame.draw.rect(screen, BLACK, (PIPE_X, TANK_Y + TANK_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT + PIPE_EXTENSION), 2)
    
    if st.session_state.filling:
        pygame.draw.rect(screen, DARK_BLUE, (PUMP_X, PUMP_Y, PIPE_WIDTH + 20, 30))
        pygame.draw.rect(screen, BLACK, (PUMP_X, PUMP_Y, PIPE_WIDTH + 20, 30), 2)
    else:
        pygame.draw.rect(screen, GRAY, (PUMP_X, PUMP_Y, PIPE_WIDTH + 20, 30))
        pygame.draw.rect(screen, BLACK, (PUMP_X, PUMP_Y, PIPE_WIDTH + 20, 30), 2)
    
    water_height = st.session_state.water_level
    if water_height > 0:
        water_rect = pygame.Rect(TANK_X, TANK_Y + TANK_HEIGHT - water_height, TANK_WIDTH, water_height)
        pygame.draw.rect(screen, WATER_COLOR_RGB, water_rect)
    
    pygame.draw.rect(screen, BLACK, (TANK_X, TANK_Y, TANK_WIDTH, TANK_HEIGHT), 2)
    
    if st.session_state.filling:
        if frame % 3 == 0:  
            st.session_state.water_particles.append([PIPE_X + PIPE_WIDTH // 2, RESERVOIR_Y])

    for particle in st.session_state.water_particles:
        particle[1] -= PARTICLE_SPEED
        if particle[1] < PUMP_Y:
            st.session_state.water_particles.remove(particle)
        else:
            pygame.draw.circle(screen, WATER_COLOR_RGB, (particle[0], particle[1]), 3)

    current_work = calculate_work(st.session_state.water_level)
    
    stats_box = pygame.Surface((200, 80))
    stats_box.fill(WHITE)
    pygame.draw.rect(stats_box, BLACK, stats_box.get_rect(), 2)
    
    FONT = pygame.font.Font(None, 30)
    progress = (st.session_state.water_level / ACTUAL_MAX_HEIGHT) * 100 if ACTUAL_MAX_HEIGHT > 0 else 0
    progress = min(100, progress)
    
    PROGRESS_TEXT = FONT.render(f"Fill Level: {progress:.1f}%", True, BLACK)
    WORK_TEXT = FONT.render(f"Work: {current_work/1000:.1f} kJ", True, BLACK)
    
    stats_box.blit(PROGRESS_TEXT, (10, 10))
    stats_box.blit(WORK_TEXT, (10, 40))
    
    screen.blit(stats_box, (WIDTH - 220, 20))
    
    return screen

frame_count = 0

while st.session_state.filling and st.session_state.water_level < ACTUAL_MAX_HEIGHT:

    next_level = st.session_state.water_level + FILLING_SPEED
    
    if next_level >= ACTUAL_MAX_HEIGHT:
        st.session_state.water_level = ACTUAL_MAX_HEIGHT
    else:
        st.session_state.water_level = next_level
        
    screen_surface = draw_ui(frame_count)
    
    frame_array = pygame.surfarray.array3d(screen_surface)  
    frame_array = np.rot90(frame_array, -1) 
    frame_array = np.fliplr(frame_array)
    frame_image = Image.fromarray(frame_array.astype('uint8')) 
    
    image_placeholder.image(
        frame_image,
        caption="Water Tank Simulation",
        use_container_width=True
    )
    
    frame_count += 1 
    time.sleep(0.1)

final_surface = draw_ui(frame_count)
frame_array = pygame.surfarray.array3d(final_surface)  
frame_array = np.rot90(frame_array, -1) 
frame_array = np.fliplr(frame_array)
frame_image = Image.fromarray(frame_array.astype('uint8')) 
image_placeholder.image(
    frame_image,
    caption="Water Tank Simulation",
    use_container_width=True
)

