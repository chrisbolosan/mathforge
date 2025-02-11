import sympy as sp

# Ex: Suppose a cylindrical water tank 4 meters high with a radius of 2 meters is located on a tower so that the bottom of the tank is
# 10 meters above the level of a stream (see figure below). How much work is done in filling the tank hal

y = sp.Symbol('y')


weight_density = 9800   #newtons per cubic meter
radius = 2  # meters
height = 4  # meters
bottom_height = 10  # meters

# volume of the cylinder per slice
volume_element = (sp.pi * radius**2) * sp.Symbol('dy')

# Force calculuations
force = weight_density * volume_element

# work done in terms of y integrations
distance = y  # distance the water is lifted here in terms of height which is y
work_integral = sp.integrate(force * distance, (y, bottom_height, bottom_height + height/2))

work_done = work_integral.simplify()

print(f"Amount of work done to fill the tank halfway: {work_done} N-meters")
