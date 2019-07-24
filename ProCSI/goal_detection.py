from turtle import *
from math import *

goal = (200, 200)

color("blue")
positionX = position()[0]
positionY = position()[1]

def euclidianDist(point1, point2):

  dist = sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
  return dist

def goalCheck(currPosition, goal):
  threshold = 50
  if euclidianDist(currPosition, goal) < threshold:
    return True 
  else:
    return False

######## from homemade_controller.py
def getUserInput():
  userInput = raw_input("Enter a command: ")
  while userInput not in ["a", "d", "w", "x"]:
    print("\nPlease enter valid command \n a/d for left/right \n w/x for forward/backward \n")
    userInput = raw_input("Enter a command: ")
  return userInput

def move(command):
  if command=="a":
    left(45)
  elif command=="d":
    right(45)
  elif command=="w":
    forward(50)
  elif command=="x":
    backward(50)
######## 


atGoal = False
while not atGoal:
  print "Goal at: ", goal
  print "Current position is: ", position()
  print "Current heading is:", heading()
  char = getUserInput()
  print("")
  move(char)
  atGoal = goalCheck(position(), goal)

print "goal reached!"

