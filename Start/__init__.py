import threading
import time
import os
import csv


# Let's make a thread class that will run our main counter
class Counter(threading.Thread):
    def __init__(self, uid, name):
        threading.Thread.__init__(self)
        self.uid = uid
        self.name = name

    def run(self):
        global core
        core = 0
        while True:
            core += modifier
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


# A class that will create and handle any modifiers to the counter.
class ModifyCounter:
    def __init__(self, name):
        self.name = name
        self.value = 1

    # A function to increase the modifier variable and make the counter go up slower.
    # It accepts arguments from get_input() and will take action on the first item in the arguments
    def increase(self, arguments):
        global modifier
        if arguments is None:
            self.modify(1)
        else:
            try:
                self.modify(int(arguments[0]))
            except ValueError:
                print("Invalid command format - you must specify a number, not a word: increase (number)")
            except TypeError:
                print("Invalid command format - you must specify a number, not a word: increase (number)")

    # A function to decrease the modifier variable and make the counter go up slower.
    # It accepts arguments from get_input() and will take action on the first item in the arguments
    def decrease(self, arguments):
        global modifier
        if arguments is None:
            self.modify(-1)
        else:
            try:
                self.modify(-(int(arguments[0])))
            except ValueError:
                print("Invalid command format - you must specify a number, not a word: decrease (number)")
            except TypeError:
                print("Invalid command format - you must specify a number, not a word: decrease (number)")

    # A function to commit the change to the modifier
    def modify(self, value):
        global modifier
        modifier += value
        if modifier < 0:
            print('Cannot decrease the increment below 0, so we\'re setting the increment to 0.')
            modifier = 0


# Let's create a class for resources so you can perform the same actions on different resources
class Resources:
    def __init__(self, name, cost):
        self.name = name
        self.quantity = 0
        self.cost = cost

    def gather(self, amount):
        global core

        try:
            amount = int(amount)
        except (TypeError, ValueError):
            print('Improper syntax, proper example is: gather wood 2')
            return

        if type(amount) is not int or amount <= 1:
            buyingquantity = 1
        else:
            buyingquantity = amount
        if core >= (self.cost * buyingquantity):
            self.quantity += buyingquantity
            core -= (self.cost * buyingquantity)
        else:
            print('You don\'t have enough money!')
            print('This '+self.name+' costs '+str(self.cost * buyingquantity)+', but you only have '+str(core)+'.')


# A simple function to check what our counter is at.
# Also shows how much the counter is increasing by.
def check(arguments):
    print('Money: '+str(core))
    print('Increasing by '+str(modifier)+' per second')
    print('Resources: ')
    for line in listResources:
        print(line + " : " + str(dictResources[line].quantity))


# A function to stop the program when called.
def stop(arguments):
    os._exit(1)


# A function that will list all commands available in the dictionary commands
def get_help(arguments):
    for entry in help_explanations:
        print(entry)


# Let's save the progress of the counter
def save(arguments):
    savedata = [core]
    for resource in dictResources:
        savedata.append(dictResources[resource].quantity)
    with open('pydle.sav', 'w+') as savefile:
        savewriter = csv.writer(savefile, delimiter='+')
        savewriter.writerow(savedata)


# Let's load the progress of the counter from the savefile
def load(arguments):
    global core
    with open('pydle.sav', 'r+') as savefile:
        readdata = csv.reader(savefile, delimiter='+')
        for row in readdata:  # NOTE: If you add another row, you'll need to change this...
            core = int(row[0])
            del row[0]
            for i in range(len(row)):
                for resource in dictResources:
                    dictResources[resource].quantity = int(row[i])


# Let's write a function to check syntax for gather and pass it to the right place.
def gather(arguments):
    if arguments[0] in dictResources:
        if len(arguments) >= 2:
            dictResources[arguments[0]].gather(arguments[1])
        else:
            dictResources[arguments[0]].gather(1)
    else:
        print('Invalid resource name.')
        print('Available resources to gather: ')
        for line in listResources:
            print(line)


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
        commands[command[0]](None)
    else:
        print("Command not found. Please try again")


# Instantiating support class objects like the main modifier
MainModifier = ModifyCounter('main')

# A dictionary that gives us a list of references to functions
commands = {
    "check": check,
    "exit": stop,
    "increase": MainModifier.increase,
    "decrease": MainModifier.decrease,
    "help": get_help,
    "save": save,
    "gather": gather,
    "load": load
}

# Instantiate all resources for the Resources class
wood = Resources('wood', 100)

# A list of resources
listResources = [
    'wood'
]

# A dictionary of the referenced class objects for resources
dictResources = {
    "wood": wood
}

# A list based on the command dictionary that gives short descriptions of the commands available.
help_explanations = [
    "check: check on the current counter.",
    "exit: exit the program",
    "increase: increase the increment of the counter",
    "decrease: decrease the increment of the counter",
    "save: save the counter\'s value",
    "load: load the counter\'s value",
    "gather: use your energy to gather materials. Available materials: wood"
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
