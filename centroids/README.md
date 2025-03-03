# Centroids

## Introduction

The centroid (or geometric center) is the average position of all the points in a shape. It is often referred to as the "center of mass" or "center of gravity" in physics.

## What is a Centroid?

The centroid of a region is the point where the region would balance if it were made of a uniform material. For a two-dimensional shape, the centroid (C) has coordinates (x̄, ȳ).

## Finding the Centroid

To find the centroid of a region bounded by the graph of a function, we use the following formulas:

### For a Region Bounded by y = f(x) from x = a to x = b

1. **x̄ (x-coordinate of the centroid):**
   x̄ = (1/A) ∫[a to b] x f(x) dx
2. **ȳ (y-coordinate of the centroid):**
   ȳ = (1/A) ∫[a to b] (f(x))^2 / 2 dx
3. **A (Area of the region):**
   A = ∫[a to b] f(x) dx

### Steps to Find the Centroid

1. **Determine the bounds (a and b):** Identify the interval [a, b] over which the function is defined.
2. **Calculate the area (A):** Integrate the function f(x) over the interval [a, b].
3. **Calculate x̄:** Integrate x times the function f(x) over the interval [a, b] and divide by the area.
4. **Calculate ȳ:** Integrate the square of the function f(x) divided by 2 over the interval [a, b] and divide by the area.

## Example

Consider the region bounded by the function y = x^2 from x = 0 to x = 1.

1. **Calculate the area (A):**
   A = ∫[0 to 1] x^2 dx = [x^3 / 3] from 0 to 1 = 1/3

2. **Calculate x̄:**
   x̄ = (1/A) ∫[0 to 1] x \* x^2 dx = 3 ∫[0 to 1] x^3 dx = 3 [x^4 / 4] from 0 to 1 = 3/4

3. **Calculate ȳ:**
   ȳ = (1/A) ∫[0 to 1] (x^2)^2 / 2 dx = 3 ∫[0 to 1] x^4 / 2 dx = (3/2) [x^5 / 5] from 0 to 1 = 3/10

Therefore, the centroid of the region is at (3/4, 3/10).

## Conclusion

Understanding how to find the centroid of a region is a fundamental skill. By following the steps outlined above, you can determine the centroid for any region bounded by a function.
