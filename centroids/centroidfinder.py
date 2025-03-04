# Find the area for the given shapes. Use symmetry to help locate the center of mass whenever possible.
#[T] Lens: y=x^2 abd y=x

import sympy as sp

x=sp.Symbol('x')

y=x**2
y=x

# functions under the curve. If horizontal bar, use y=f(x), if vertical bar, use x=f(y)
f1 =x
f2 = x**2

#intersection points against x-axis
INTERSECTION_POINTS = sp.solve(f1-f2,x)

x0, x1 = INTERSECTION_POINTS

# total area

M = sp.integrate(f1-f2, (x,x0,x1))

#moments
