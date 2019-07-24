import turtle

t = turtle.Turtle()
t.color("blue")

def getUserInput():
  user = raw_input("Enter a command: ")
  return user

def move(command):
  print(command)
  if command=="a":
    left()
  elif command=="d":
    right()
  elif command=="w":
    forward()
  elif command=="x":
    backward()

def forward():
    t.forward(100)

def backward():
    t.backward(100)

def left():
    t.left(30)

def right():
    t.right(30)

char = ""
while char != "q":
  char = getUserInput()
  move(char)
  #print(t.position())