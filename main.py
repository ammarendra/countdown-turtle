import turtle
import random

# set turtle
turtle.width(2)
turtle.speed(10)
  
# loop for pattern
for i in range(10):
    turtle.circle(40)
    turtle.right(36)
  
# set screen and drawing remain as it is.
turtle.screensize(canvwidth=400, canvheight=300,
                  bg="blue")