import threading
import time
import os
import csv
import tkinter as tk
import tkinter.ttk as ttk


# Global static variables
spacing_PadY = 5
spacing_PadX = 5


class Counter(threading.Thread):
    # This class is used to run a thread for the money counter so it may run unimpeded
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            while money.value < (money.value + money.modifier.netvalue):
                increment = money.modifier.netvalue
                time.sleep(.1)
                newWindow.frames['MainPage'].update()
                money.value += round(increment / money.modifier.netspeed, 1)


class Progress(threading.Thread):
    # This class is used to run a thread for the money counter so it may run unimpeded
    def __init__(self):
        super(Progress, self).__init__()
        self.daemon = True
        self.paused = True
        self.state = threading.Condition()

    def run(self):
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()
            newWindow.frames['MainPage'].button_click.config(text="WORK FASTER!!",
                                                             command=lambda: ProgressThread.accelerate())
            newWindow.update_idletasks()
            while newWindow.frames['MainPage'].progressbar_work['value'] <= 100:
                newWindow.frames['MainPage'].progressbar_work['value'] += (10/money.clickmodifier.netspeed)
                newWindow.update_idletasks()
                time.sleep(.1)
            money.increase(newWindow, 'value', money.clickmodifier.netvalue)
            newWindow.frames['MainPage'].progressbar_work['value'] = 0
            newWindow.frames['MainPage'].button_click.config(text="WORK",
                                                             command=lambda: ProgressThread.resume())
            newWindow.update_idletasks()
            self.pause()

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()

    def pause(self):
        with self.state:
            self.paused = True

    def accelerate(self):
        with self.state:
            if not self.paused:
                newWindow.frames['MainPage'].progressbar_work['value'] += 10


class ValueVar:
    def __init__(self, grossvalue: int, flatbonus: float, pctbonus: float, flatupgrcost: float,
                 pctupgrcost: float, grossspeed: int, flatspeedbonus: float, pctspeedbonus: float,
                 flatspeedupgrcost: float, pctspeedupgrcost: float) -> None:
        self.grossvalue = grossvalue
        self.flatbonus = flatbonus
        self.pctbonus = pctbonus
        self.flatupgrcost = flatupgrcost
        self.pctupgrcost = pctupgrcost
        self.grossspeed = grossspeed
        self.flatspeedbonus = flatspeedbonus
        self.pctspeedbonus = pctspeedbonus
        self.flatspeedupgrcost = flatspeedupgrcost
        self.pctspeedupgrcost = pctspeedupgrcost
        self.netvalue = (grossvalue + flatbonus) * pctbonus
        self.netspeed = (grossspeed + flatspeedbonus) * pctspeedbonus


class Value:
    # This class is used to track the objects used in the game, such as money and resources.
    # It just helps keep things tidy and consistent across types of objects.
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.value = 0.0                                             # The actual amount of X object
        self.modifier = ValueVar(1, 0, 1, 25, 1.1, 10, 0, 1, 25, 1.1)
        self.clickmodifier = ValueVar(10, 0, 1, 25, 1.1, 60, 0, 1, 25, 1.1)

    def update(self, attribute=("modifier", "clickpower")):
        for i in attribute:
            if i == "modifier":
                setattr(self.modifier, "netvalue", (money.modifier.grossvalue + money.modifier.flatbonus)
                        * money.modifier.pctbonus)
            if i == "clickpower":
                setattr(self.clickmodifier, "netvalue", (money.clickmodifier.grossvalue + money.clickmodifier.flatbonus)
                        * money.clickmodifier.pctbonus)

    def increase(self, frame, attribute="value", amount=1.0):
        """
        Adds a value to an attribute inside the referenced class object
        :param attribute: The attribute you want to modify
        :param amount: The amount you want to add to that attribute
        :param frame: The frame where a label exists that shows this value, used to call the update method in it
        :return: null
        """
        modify_value = getattr(self, attribute)
        modify_value += amount
        setattr(self, attribute, modify_value)
        frame.frames['MainPage'].update()

    def decrease(self, frame, attribute="value", amount=1):
        """
        Subtracts a value from as attribute inside the referenced class object
        :param attribute: The attribute you want to modify
        :param amount: The amount you want to subtract from that attribute
        :param frame: The frame where a label exists that shows this value, used to call the update method in it
        :return: null
        """
        modify_value = getattr(self, attribute)
        if modify_value - amount <= 0:
            modify_value = 0
        else:
            modify_value -= amount
        setattr(self, attribute, modify_value)
        frame.frames['MainPage'].update()

    def upgrade(self, frame, attribute="modifier", amount=1):
        """
        :param frame: The frame where a label exists that shows this value, used to call the update method in it
        :param attribute: The attribute you want to upgrade
        :param amount: The amount of times to upgrade the attribute
        :return:
        """
        if attribute == "modifier":
            if self.value >= round(self.modifier.flatupgrcost, 1):
                self.value -= round(self.modifier.flatupgrcost, 1)
                self.modifier.flatupgrcost = round(self.modifier.flatupgrcost * self.modifier.pctupgrcost, 1)
                self.modifier.flatbonus += amount
                frame.frames['MainPage'].update()
        if attribute == "clickpower":
            if self.value >= round(self.clickmodifier.flatupgrcost, 1):
                self.value -= round(self.clickmodifier.flatupgrcost, 1)
                self.clickmodifier.flatupgrcost = round(self.clickmodifier.flatupgrcost *
                                                        self.clickmodifier.pctupgrcost, 1)
                self.clickmodifier.flatbonus += amount
                frame.frames['MainPage'].update()

    def downgrade(self, frame, attribute="modifier", amount=1):
        if attribute == "modifier":
            if self.modifier.flatbonus > 0:
                self.value += round(self.modifier.flatupgrcost, 1)
                self.modifier.flatupgrcost = round(self.modifier.flatupgrcost / self.modifier.pctupgrcost, 1)
                self.modifier.flatbonus -= amount
                frame.frames['MainPage'].update()
        if attribute == "clickpower":
            if self.clickmodifier.flatbonus > 0:
                self.value += round(self.clickmodifier.flatupgrcost, 1)
                self.clickmodifier.flatupgrcost = round(self.clickmodifier.flatupgrcost /
                                                        self.clickmodifier.pctupgrcost, 1)
                self.clickmodifier.flatbonus -= amount
                frame.frames['MainPage'].update()


class PageManager(tk.Tk):

    def __init__(self, *args, **kwargs):
        """
        This makes a container that will hold all of our frames.
        The visible frame will be managed by which one is on top of the stack.
        :param args: null
        :param kwargs: null
        """
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for page in (StartPage, MainPage, OptionsPage):
            page_name = page.__name__
            frame = page(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """
        Raises the given page's frame to the top of the stack
        :param page_name: Must be a name assigned to a frame in self.frames, see __init__
        :return: null
        """
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        """
        Assigns the layout for the menu seen when starting the game
        :param parent: Assigned to container from class PageManager __init__
        :param controller: Assigned to an instance of PageManager from class PageManager __init__
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to Pydle!")
        label.pack(side="top", fill="x", pady=10)

        button_start = tk.Button(self, text="Start Game",
                                 command=lambda: controller.show_frame("MainPage"))
        button_quit = tk.Button(self, text="Quit",
                                command=stop)
        button_quit.pack(fill='x', side='bottom', padx=spacing_PadX, pady=spacing_PadY*2)
        button_start.pack(fill='x', side='bottom', padx=spacing_PadX, pady=spacing_PadY*2)


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        """
        Assigns the layout for the main game-play page
        :param parent: Assigned to container from class PageManager __init__
        :param controller: Assigned to an instance of PageManager from class PageManager __init__
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # MONEY FRAME
        self.labelframe_money = tk.LabelFrame(self, text="MONEY")
        self.labelframe_money.pack(expand=0, fill='x', side='top', padx=spacing_PadX/2, pady=spacing_PadY/2)

        self.label_counter = tk.Label(self.labelframe_money, text=round(money.value, 0))
        self.label_counter.pack(side='top', padx=spacing_PadX, pady=spacing_PadX/2)

        self.label_modifier = tk.Label(self.labelframe_money,
                                       text="Earning " + str(money.modifier.netvalue) + " per second")
        self.label_modifier.pack(side='top', padx=spacing_PadX, pady=spacing_PadX/2)

        # Common buttons
        button_options_resolution = tk.Button(self, text='Quit to Main Menu',
                                              command=lambda: controller.show_frame("StartPage"))
        button_options_resolution.pack(fill='x', side='bottom', padx=spacing_PadX, pady=spacing_PadY)
        button_options_close = tk.Button(self, text='Options', command=lambda: controller.show_frame("OptionsPage"))
        button_options_close.pack(fill='x', side='bottom', padx=spacing_PadX, pady=spacing_PadY)

        # UPGRADE FRAME
        labelframe_upgrades = tk.LabelFrame(self, text="UPGRADES")
        labelframe_upgrades.pack(expand=1, fill='both', side='right', padx=spacing_PadX, pady=spacing_PadY)
        # MPS FRAME
        labelframe_money_per_second = tk.LabelFrame(labelframe_upgrades, text="Money per Second")
        labelframe_money_per_second.pack(fill='x', side='top', padx=spacing_PadX, pady=spacing_PadY)
        # BUY BUTTON
        self.button_purchase = tk.Button(labelframe_money_per_second, text="BUY - 25",
                                         command=lambda: money.upgrade(newWindow))
        self.button_purchase.pack(fill='x', side='top', padx=spacing_PadX, pady=spacing_PadX)
        # SELL BUTTON
        self.button_sell = tk.Button(labelframe_money_per_second, text="SELL - 25",
                                     command=lambda: money.downgrade(newWindow))
        self.button_sell.pack(fill='x', side='top', padx=spacing_PadX, pady=spacing_PadX)

        # MPC FRAME
        labelframe_money_per_click = tk.LabelFrame(labelframe_upgrades, text="Money per Click")
        labelframe_money_per_click.pack(fill='x', side='top', padx=spacing_PadX, pady=spacing_PadY)
        # BUY BUTTON
        self.button_purchase_click = tk.Button(labelframe_money_per_click, text="BUY",
                                               command=lambda: money.upgrade(newWindow, 'clickpower'))
        self.button_purchase_click.pack(fill='x', side='top', padx=spacing_PadX, pady=spacing_PadX)
        # SELL BUTTON
        self.button_sell_click = tk.Button(labelframe_money_per_click, text="SELL",
                                           command=lambda: money.downgrade(newWindow, 'clickpower'))
        self.button_sell_click.pack(fill='x', side='top', padx=spacing_PadX, pady=spacing_PadX)

        # CLICK FRAME
        labelframe_click = tk.LabelFrame(self, text="WORK FOR MONEY")
        labelframe_click.pack(expand=1, fill='both', side='right', padx=spacing_PadX, pady=spacing_PadY)

        self.progressbar_work = ttk.Progressbar(labelframe_click, orient='horizontal', length=100,
                                                mode='determinate', maximum=100)
        self.progressbar_work.pack(fill='x', side='top', padx=spacing_PadX, pady=spacing_PadY)

        self.button_click = tk.Button(labelframe_click, text="WORK",
                                      command=lambda: ProgressThread.resume())
        self.button_click.pack(fill='x', side='top', padx=spacing_PadX, pady=spacing_PadY)

        self.label_clickpower = tk.Label(labelframe_click,
                                         text="Earning " + str(money.clickmodifier.netvalue) + " per shift")
        self.label_clickpower.pack(side='top', padx=spacing_PadX, pady=spacing_PadY)

    def update(self):
        """
        Updates class variables used on the labels, then updates the text on labels.
        Usually ran after changes to values that are present on the labels.
        :return: null
        """
        money.update()
        self.label_counter.config(text=round(money.value, 0))
        self.label_modifier.config(text="Earning " + str(money.modifier.netvalue) + " per second")
        self.label_clickpower.config(text="Earning " + str(money.clickmodifier.netvalue) + " per shift")
        self.button_purchase.config(text="BUY - " + str(money.modifier.flatupgrcost))
        self.button_sell.config(text="SELL - " + str(money.modifier.flatupgrcost))
        self.button_purchase_click.config(text="BUY - " + str(money.clickmodifier.flatupgrcost))
        self.button_sell_click.config(text="SELL - " + str(money.clickmodifier.flatupgrcost))


class OptionsPage(tk.Frame):

    def __init__(self, parent, controller):
        """
        Assigns the layout for the menu seen when adjusting game settings
        :param parent: Assigned to container from class PageManager __init__
        :param controller: Assigned to an instance of PageManager from class PageManager __init__
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Frame for settings
        labelframe_options = tk.LabelFrame(self, text='Game Settings')
        labelframe_options.pack(fill='both', side='top', padx=spacing_PadX, pady=spacing_PadY)
        # Resolution option menu
        label_options_resolution = tk.Label(labelframe_options, text='Resolution')
        label_options_resolution.pack(side='left', padx=spacing_PadX, pady=spacing_PadY)
        current_resolution = tk.StringVar(labelframe_options)
        current_resolution.set("640x480")
        listbox_options_resolutions = tk.OptionMenu(labelframe_options, current_resolution, "640x480", "800x480",
                                                    "1280x800")
        listbox_options_resolutions.pack(expand=1, fill='x', side='left', padx=spacing_PadX, pady=spacing_PadY)

        # Common buttons
        button_options_close = tk.Button(self, text='Close', command=lambda: controller.show_frame("MainPage"))
        button_options_close.pack(fill='x', side='bottom', padx=spacing_PadX, pady=spacing_PadY)
        button_options_resolution = tk.Button(self, text='Apply',
                                              command=lambda: configure_newwindow(current_resolution.get()))
        button_options_resolution.pack(fill='x', side='bottom', padx=spacing_PadX, pady=spacing_PadY)

        # Frame for file operations
        labelframe_file = tk.LabelFrame(self, text='Save, Load, Reset')
        labelframe_file.pack(fill='both', side='top', padx=spacing_PadX, pady=spacing_PadY)
        # Save button
        button_save = tk.Button(labelframe_file, text='Save Game', command=save)
        button_save.pack(fill='x', side='top', padx=spacing_PadX, pady=spacing_PadY*2)
        # Load button
        button_save = tk.Button(labelframe_file, text='Load Game', command=load)
        button_save.pack(fill='x', side='top', padx=spacing_PadX, pady=spacing_PadY)


def stop():
    """
    Exits the application.
    :return: null
    """
    os._exit(1)                                                          # I know, it's naughty...


def save():
    """
    Writes the current values of dictionary_resources to a csv for use later.
    :return: null
    """
    savedata = []
    with open('pydle.sav', 'w+', newline='') as savefile:
        savewriter = csv.writer(savefile, delimiter='+')
        for key in dictionary_resources:
            for var in sorted(vars(dictionary_resources[key])):
                if 'ValueVar' in str(getattr(dictionary_resources[key], var)):
                    continue
                else:
                    savedata.append(str(getattr(dictionary_resources[key], var)))
            savewriter.writerow(savedata)
            savedata = []
            for var in sorted(vars(dictionary_resources[key])):
                savedata = []
                try:
                    for subvar in sorted(vars(getattr(dictionary_resources[key], var))):
                        savedata.append(str(getattr(getattr(dictionary_resources[key], var), subvar)))
                    savewriter.writerow(savedata)
                except TypeError:
                    continue
            savewriter.writerow(['break'])


def load():
    """
    Reads the values of an external csv and imports them to values in dictionary_resources
    :return: null
    """
    with open('pydle.sav', 'r+') as savefile:
        readdata = csv.reader(savefile, delimiter='+')
        loaddata = []
        for row in readdata:
            loaddata.append(row)
    resourcecount = 0
    varcount = 0
    for row in loaddata:
        targetvar = dictionary_resources[list_resources[resourcecount]]
        if row[0] == 'resource':
            for var in sorted(vars(targetvar)):
                if 'ValueVar' in str(getattr(targetvar, var)):
                    continue
                else:
                    if type(getattr(targetvar, var)) is str:
                        setattr(targetvar, var, str(row[0]))
                    elif type(getattr(targetvar, var)) is int:
                        try:
                            setattr(targetvar, var, int(row[0]))
                        except ValueError:
                            setattr(targetvar, var, float(row[0]))
                    elif type(getattr(targetvar, var)) is float:
                        setattr(targetvar, var, float(row[0]))
                    del row[0]
        elif row[0] == 'break':
            resourcecount += 1
            varcount = 0
        else:
            targetsubvar = sorted(list_valuevars)[varcount]
            if 'ValueVar' in str(getattr(targetvar, targetsubvar)):
                for subvar in sorted(vars(getattr(targetvar, targetsubvar))):
                    if type(getattr(getattr(targetvar, targetsubvar), subvar)) is str:
                        setattr(getattr(targetvar, targetsubvar), subvar, str(row[0]))
                    elif type(getattr(getattr(targetvar, targetsubvar), subvar)) is int:
                        try:
                            setattr(getattr(targetvar, targetsubvar), subvar, int(row[0]))
                        except ValueError:
                            setattr(getattr(targetvar, targetsubvar), subvar, float(row[0]))
                    elif type(getattr(getattr(targetvar, targetsubvar), subvar)) is float:
                        setattr(getattr(targetvar, targetsubvar), subvar, float(row[0]))
                    del row[0]
                varcount += 1


def configure_newwindow(resolution):
    newWindow.geometry(resolution)
    newWindow.update()


# Class instantiations
money = Value("money", "resource")

# Instantiate an instance of PageManager
newWindow = PageManager()
newWindow.geometry('640x480')
newWindow.title('Pydle!')

# Resource list - Used to iterate through the dictionary for resources
list_resources = [
    "money"
]

# Resource dictionary - Helpful to keep track of members from class Value
dictionary_resources = {
    "money": money
}

# ValueVar list - Helpful to load in values from save files
list_valuevars = [
    'clickmodifier', 'modifier'
]

# Thread instantiations
CounterThread = Counter()
ProgressThread = Progress()

# Start Threads
CounterThread.start()
ProgressThread.start()

# Start main window
newWindow.mainloop()
