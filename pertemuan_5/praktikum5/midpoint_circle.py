
def midpoint_circle(radius):
    x = 0
    y = radius
    p = 0 - radius
    points = []

    while x <= y:
        points.extend([
            ( x, y), (y, x), (-x, y), (-y, x), (x, -y), (y, -x), (-x, -y), (-y, -x)
        ])

        x += 1
        if p < 0:
            p = p + 2*x + 3  
        else:
            y -= 1
            p = p + 2*(x - y) + 5

    return points

import turtle

def draw_points(points, scale=20):
    turtle.speed(0)
    turtle.penup()
    turtle.hideturtle()

    turtle.goto(0,0)
    turtle.dot(6, "red")

    for x, y in points:
        turtle.goto(x * scale, y * scale)
        turtle.dot(6, "black") 

    turtle.done()

r = 6
points = midpoint_circle(r)
draw_points(points)