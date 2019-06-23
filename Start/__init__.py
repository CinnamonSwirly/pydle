import threading
import time
import os


# Let's make a thread class that will run our main counter
class Counter(threading.Thread):
    def __init__(self, uid, name):
        threading.Thread.__init__(self)
        self.uid = uid
        self.name = name

    def run(self):
        global store
        store = 0
        while True:
            store += modifier
            time.sleep(1)


# This class will calculate the number by which we increment the central number in Counter
class Modifier(threading.Thread):
    def __init__(self, uid, name):
        threading.Thread.__init__(self)
        self.uid = uid
        self.name = name

    def run(self):
        global modifier
        modifier = 1


# A simple function to check what our counter is at.
def check():
    print(store)


# A function to stop the program when called.
def stop():
    os._exit(1)


# A function to increase the modifier variable and make the counter go up faster.
def increase():
    global modifier
    modifier += 1


# A function to decrease the modifier variable and make the counter go up slower.
# TODO: Make it so the variable can't be decreased below 0.
def decrease():
    global modifier
    modifier -= 1


# A function that will get the user's input and, if the input matches a command, executes the command.
# TODO: Pass data from the input into functions
# TODO: Create a help command to list all commands
def get_input():
    print("Enter a command:")
    command = input().split()
    if command[0] in commands:
        commands[command[0]]()
    else:
        print("Command not found. Please try again")


# A dictionary that gives us a list of references to functions
commands = {
    "check": check,
    "exit": stop,
    "increase": increase,
    "decrease":decrease
}

# Create the threads
ModifierThread = Modifier(1, "Modifier")
CounterThread = Counter(2, "Counter")

# Start the threads
ModifierThread.start()
CounterThread.start()

# Let the user choose before checking on the counter
while True:
    get_input()
