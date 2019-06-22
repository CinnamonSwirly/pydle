import threading
import time


# Let's make a thread class that will run our main counter
class CounterThread(threading.Thread):
    def __init__(self, uid, name):
        threading.Thread.__init__(self)
        self.uid = uid
        self.name = name

    def run(self):
        global store
        store = 0
        while True:
            store += 1
            time.sleep(1)


# A simple function to check what our counter is at.
def inquire():
    print(store)


# Create the main thread
MainThread = CounterThread(1, "MainThread")
# Start the main thread
MainThread.start()
# Loop to wait 3 seconds before checking on the counter
while True:
    input('Press enter to check on the counter...')
    inquire()
