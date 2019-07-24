from turtle import *

penup() # don't draw anything until at desired location

goto(50, 50) # (x, y) coordinates
goto(-50, 50)
goto(100, -50)
goto(-50, -50)

pendown() # start drawing now
forward(100)
setheading(45) # heading in degrees
forward(80)
