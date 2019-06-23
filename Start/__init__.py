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
# It is very simple right now, but as the calculations get heavier, a separate thread is best.
class Modifier(threading.Thread):
    def __init__(self, uid, name):
        threading.Thread.__init__(self)
        self.uid = uid
        self.name = name

    def run(self):
        global modifier
        modifier = 1


# A simple function to check what our counter is at.
# Also shows how much the counter is increasing by.
def check():
    print(store)
    print('Increasing by '+str(modifier)+' per second')


# A function to stop the program when called.
def stop():
    os._exit(1)


# A function to increase the modifier variable and make the counter go up faster.
# TODO: Accept arguments
def increase():
    global modifier
    modifier += 1


# A function to decrease the modifier variable and make the counter go up slower.
# The function won't let the modifier variable go below zero.
# TODO: Accept arguments
def decrease():
    global modifier
    if modifier >= 1:
        modifier -= 1
    else:
        print('Cannot decrease the increment below 0!')


# A function that will list all commands available in the dictionary commands
def get_help():
    for entry in help_explanations:
        print(entry)


# A function that will get the user's input and, if the input matches a command, executes the command.
# The function collects user arguments as anything past the first word and passes the whole list to the function called.
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
    "decrease": decrease,
    "help": get_help
}

# A list based on the command dictionary that gives short descriptions of the commands available.
help_explanations = [
    "check: check on the current counter.",
    "exit: exit the program",
    "increase: increase the increment of the counter",
    "decrease: decrease the increment of the counter",
    "help: what you\'re looking at right now"
]

# Create the threads
ModifierThread = Modifier(1, "Modifier")
CounterThread = Counter(2, "Counter")

# Start the threads - Modifier has to start first or else the modifier variable isn't defined for the counter.
ModifierThread.start()
CounterThread.start()

# Let the user choose before checking on the counter
while True:
    get_input()
