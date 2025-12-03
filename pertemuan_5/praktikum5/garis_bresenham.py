import turtle
from line import bresenham_line

def draw_points(points, scale=20):
    turtle.speed(0)
    turtle.penup()
    turtle.hideturtle()
    for x, y in points:
        turtle.goto(x * scale, y * scale)
        turtle.dot(6, "red")
    turtle.done()

points = bresenham_line(-17, 0, 17, 0)
draw_points(points)