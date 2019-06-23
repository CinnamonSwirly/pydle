import threading
import time
import os


# Let's make a thread class that will run our main counter
# TODO: Show how much the counter is increasing per second
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
# The function won't let the modifier variable go below zero.
def decrease():
    global modifier
    if modifier >= 1:
        modifier -= 1
    else:
        print('Cannot decrease the increment below 0!')


# A function that will get the user's input and, if the input matches a command, executes the command.
# The function collects user arguments as anything past the first word and passes the whole list to the function called.
# TODO: Create a help command to list all commands
def get_input():
    print("Enter a command: ")
    command = input().split()
    if len(command) >= 2 and command[0] in commands:
        call_command = command[0]
        del command[0]
        commands[call_command](command)
    elif command[0] in commands:
        commands[command[0]]()
    else:
        print("Command not found. Please try again")


# A dictionary that gives us a list of references to functions
commands = {
    "check": check,
    "exit": stop,
    "increase": increase,
    "decrease": decrease
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
