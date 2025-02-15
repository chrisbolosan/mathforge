import sympy as sp

# Ex: Suppose a cylindrical water tank 4 meters high with a RADIUS of 2 meters is located on a tower so that the bottom of the tank is
# 10 meters above the level of a stream (see figure below). How much work is done in filling the tank hal

y = sp.Symbol('y')


WEIGHT_DENSITY = 9800   #newtons per cubic meter
RADIUS = 2  # meters
HEIGHT = 4  # meters
BOTTOM_HEIGHT = 10  # meters

# volume of the cylinder per slice
VOLUME_ELEMENT = (sp.pi * RADIUS**2) * sp.Symbol('dy')

# FORCE calculuations
FORCE = WEIGHT_DENSITY * VOLUME_ELEMENT

# work done in terms of y integrations
DISTANCE = y  # DISTANCE the water is lifted here in terms of height which is y
WORK_INTEGRAL = sp.integrate(FORCE * DISTANCE, (y, BOTTOM_HEIGHT, BOTTOM_HEIGHT + HEIGHT/2))

WORK_DONE = WORK_INTEGRAL.simplify()

print(f"Amount of work done to fill the tank halfway: {WORK_DONE} N-meters")
