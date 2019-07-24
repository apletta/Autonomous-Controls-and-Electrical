from turtle import *

color("blue")

def getUserInput():
  userInput = raw_input("Enter a command: ")
  while userInput not in ["a", "d", "w", "x", "q"]:
    print("\nPlease enter valid command \n a/d for left/right \n w/x for forward/backward \n q to quit \n")
    userInput = raw_input("Enter a command: ")
  return userInput

def move(command):
  if command=="a":
    setheading(30)
  elif command=="d":
    setheading(-30)
  elif command=="w":
    forward(100)
  elif command=="x":
    backward(100)

char = ""
while char != "q":
  char = getUserInput()
  move(char)
  print(position())