# Find the area for the given shapes. Use symmetry to help locate the center of mass whenever possible.
#[T] Lens: y=x^2 abd y=x

import sympy as sp
from sympy import *

x=sp.Symbol('x')

# functions under the curve. If horizontal bar, use y=f(x), if vertical bar, use x=f(y)
f1 =x
f2 =x**2

#intersection points against x-axis
x_intersections = sp.solve(f1-f2,x)
x0, x1 = x_intersections

# total area
M = sp.integrate(f1-f2, (x,x0,x1))

#moments
My = sp.integrate(x*(f1-f2),(x,x0,x1))
Mx = sp.integrate(((f1+f2)/2)*(f1-f2),(x,x0,x1))

x_bar = My/M
y_bar = Mx/M

#results
print("\n===== Results =====")
print(f"Intersection Points: {x_intersections}")
print(f"Moment of Y-Axis: {My}")
print(f"Moment of X-Axis: {Mx}")
print(f"x̄: {x_bar}")
print(f"ȳ: {y_bar}")
print(f"Centroid is: ({x_bar} , {y_bar})")
