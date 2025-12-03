import turtle
from line import bresenham_line

def polygon(vertices):
    all_points = []
    n = len(vertices)
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n] 
        all_points.extend(bresenham_line(x1, y1, x2, y2))
    return all_points

def draw_points(points, scale=20):
    turtle.speed(0)
    turtle.penup()
    turtle.hideturtle()
    for x, y in points:
        turtle.goto(x * scale, y * scale)
        turtle.dot(6, "red")
    turtle.done()

vertices = [(-3, 0), (2, 0), (2, 5), (-3, 5)]  
poly_points = polygon(vertices)
draw_points(poly_points)