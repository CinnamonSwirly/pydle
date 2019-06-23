import threading
import time


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
def inquire():
    print(store)


# Create the threads
CounterThread = Counter(1, "Counter")
ModifierThread = Modifier(2, "Modifier")
# Start the threads
CounterThread.start()
ModifierThread.start()
# Let the user choose before checking on the counter
while True:
    input('Press enter to check on the counter...')
    inquire()
