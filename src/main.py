from tkinter import *
from tkinter import ttk
import re

##TO DO CLEAR CODE TO NOT REPEAT
## WRITING TO FILE
## READING FROM FILE

#list of months
MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"]

float_regex = r"^(?:[1-9]\d*(?:[.,]\d+)?|0?[.,]\d*[1-9]\d*|0)$"

class BudgetData():
    def __init__(self):
        self.costs = {month: {} for month in MONTHS}
        self.gains = {month: {} for month in MONTHS}
        pass
    
    def add_cost(self, month, name, value):
        if month not in self.costs:
            self.costs[month] = {}
        self.costs[month][name] = value
    
    def delete_cost(self, month, name):
        if month in self.costs and name in self.costs[month]:
            del(self.costs[month][name])

    def get_total_costs(self, month):
        if month in self.costs:
            return sum(self.costs[month].values())
        return 0.0
    
    def add_gains(self, month, name, value):
        if month not in self.gains:
            self.gains[month] = {}
        self.gains[month][name] = value
    
    def delete_gains(self, month, name):
        if month in self.gains and name in self.gains[month]:
            del(self.gains[month][name])

    def get_total_gains(self, month):
        if month in self.gains:
            return sum(self.gains[month].values())
        return 0.0

class Window():
    def __init__(self, root, month):
        self.root = root
        self.month = month
        self.window = None
    
    def on_exit(self):
        if self.window:
            self.window.destroy()
        self.window = None
    
    def open_window(self, title = ""):
        self.window = Toplevel(self.root)
        self.window.title(title)
        self.window.geometry("300x200")
        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)
    
    def get_active_window(self):
        if self.window is None:# and self.window.winfo_exists():
            return False
        return True


class CostsWindow(Window):
    def __init__(self, root, month, callback, costs):
        #UPDATED
        self.list_box = None
        self.cost_name = StringVar()
        self.cost_value = StringVar()
        self._callback = callback
        self.costs = costs
        super().__init__(root, month)
        self.open_window()
    
    def on_exit(self):
        super().on_exit()
        self.list_box = None

    def open_window(self):
        super().open_window(f"Costs for {self.month}")
        #Filling costs list
        self.list_box = Listbox(self.window, height=5)
        if self.month in self.costs:
            index = 0
            for key in self.costs[self.month].keys():
                self.list_box.insert(index, str(key + " => " + str(self.costs[self.month][key])))
                index += 1
        self.list_box.grid(column=0, row=0, sticky=(N, W, E, S))
        self.list_box.select_set(0)
        scrollbar = Scrollbar(self.window, orient=VERTICAL, command=self.list_box.yview)
        scrollbar.grid(column=1, row=0, sticky=(W,N,S))
        self.list_box['yscrollcommand'] = scrollbar.set


        delete_button = ttk.Button(self.window, text="Delete", default="normal", command=self.delete_element)
        delete_button.grid(column=2, row=0, sticky=(W,N))

        name_label = ttk.Label(self.window, text = "Name")
        value_label = ttk.Label(self.window, text="Value")

        name_label.grid(column=0, row=1, sticky=N)
        value_label.grid(column=1, row=1, sticky=N)

        name_entry = ttk.Entry(self.window, textvariable=self.cost_name)
        value_entry = ttk.Entry(self.window, textvariable=self.cost_value)

        name_entry.grid(column=0, row=2, sticky=N)
        value_entry.grid(column=1, row=2, sticky=N)

        add_button = ttk.Button(self.window, text="Add", default="normal", command=self.add_element)
        add_button.grid(column=0, row=3, sticky=N)

    def delete_element(self, *args):
        #UPDATED
        if self.list_box == None:
            return
        indxs = self.list_box.curselection()
        for index in indxs:
            tmp_title = self.list_box.get(index, index)[0].split("=>")[0].rstrip()
            self.list_box.delete(index, index)
            if tmp_title:
                self._callback(self.month, None, tmp_title, True)
            else:
                raise Exception("Element is missing an title")

    def add_element(self):
        #UPDATED
        global float_regex

        if self.list_box == None:
            return
        if self.cost_name.get() != "" and self.cost_value.get() != "":
            #CHECK LATER
            if not self.month in self.costs:
                self.costs[self.month] = {}

            if not re.match(float_regex, self.cost_value.get()):
                print(f"Regex failed regex: {float_regex} : value : {self.cost_value.get()}")
                #TO DO => add error message
                return
            if self.cost_name.get() in self.costs[self.month]:
                print("Name exists in costs")
                #TO DO => add error message
                return
            self.list_box.insert(self.list_box.size(), str(self.cost_name.get() + " => " + self.cost_value.get()))

            try:
                tmp_value = float(self.cost_value.get())
                self._callback(self.month, tmp_value, self.cost_name.get())
            except Exception as error:
                print(f"Error in casting string to float : {error}")
                return

            self.cost_name.set("")
            self.cost_value.set("")
        else:
            return


class GainsWindow(Window):
    def __init__(self, root, month, callback, gains):
        #UPDATED
        self.list_box = None
        self.gain_name = StringVar()
        self.gain_value = StringVar()
        self.gains = gains
        self._callback = callback
        super().__init__(root, month)
        self.open_window()
    
    def on_exit(self):
        super().on_exit()
        self.list_box = None

    def open_window(self):
        super().open_window(f"Gains for {self.month}")
        #Filling gains list
        self.list_box = Listbox(self.window, height=5)
        if self.month in self.gains:
            index = 0
            for key in self.gains[self.month].keys():
                self.list_box.insert(index, str(key + " => " + str(self.gains[self.month][key])))
                index += 1
        self.list_box.grid(column=0, row=0, sticky=(N, W, E, S))
        self.list_box.select_set(0)
        scrollbar = Scrollbar(self.window, orient=VERTICAL, command=self.list_box.yview)
        scrollbar.grid(column=1, row=0, sticky=(W,N,S))
        self.list_box['yscrollcommand'] = scrollbar.set


        delete_button = ttk.Button(self.window, text="Delete", default="normal", command=self.delete_element)
        delete_button.grid(column=2, row=0, sticky=(W,N))

        name_label = ttk.Label(self.window, text = "Name")
        value_label = ttk.Label(self.window, text="Value")

        name_label.grid(column=0, row=1, sticky=N)
        value_label.grid(column=1, row=1, sticky=N)

        name_entry = ttk.Entry(self.window, textvariable=self.gain_name)
        value_entry = ttk.Entry(self.window, textvariable=self.gain_value)

        name_entry.grid(column=0, row=2, sticky=N)
        value_entry.grid(column=1, row=2, sticky=N)

        add_button = ttk.Button(self.window, text="Add", default="normal", command=self.add_element)
        add_button.grid(column=0, row=3, sticky=N)


    def delete_element(self, *args):
        #UPDATED
        if self.list_box == None:
            return
        indxs = self.list_box.curselection()
        for index in indxs:
            tmp_title = self.list_box.get(index, index)[0].split("=>")[0].rstrip()
            self.list_box.delete(index, index)
            if tmp_title:
                self._callback(self.month, None, tmp_title, True)
            else:
                raise Exception("Element is missing an title")

    def add_element(self):
        #Updated
        global float_regex

        if self.list_box == None:
            return
        if self.gain_name.get() != "" and self.gain_value.get() != "": 
            if not self.month in self.gains:
                self.gains[self.month] = {}

            if not re.match(float_regex, self.gain_value.get()):
                raise Exception(f"Regex failed regex: {float_regex} : value : {self.gain_value.get()}")
                return
            if self.gain_name.get() in self.gains[self.month]:
                raise Exception("Name exists in gains")
                return
           
            self.list_box.insert(self.list_box.size(), str(self.gain_name.get() + " => " + self.gain_value.get()))

            try:
                tmp_value = float(self.gain_value.get())
                self._callback(self.month, tmp_value, self.gain_name.get())
            except Exception as error:
                print(f"Error in casting string to float : {error}")
                return
            self.gain_name.set("")
            self.gain_value.set("")
        else:
            return

class MainProgram():
    def __init__(self):
        self.root = Tk()
        self.configure_root()

        self.content = ttk.Frame(self.root, padding=(10, 10 , 10, 10))
        self.content.grid(column=0, row=0)

        self.data = BudgetData()

        self.open_windows_costs = {}
        self.open_windows_gains = {}

        self.display_month = StringVar(value="Month:")
        self.display_costs = StringVar(value="Costs:")
        self.display_gain = StringVar(value="Gain:")

        self.current_month = ""
        self.current_costs = 0.0
        self.current_gains = 0.0

        self.list_box = Listbox(self.content, height=5)
        self.initialize()
        self.save_to_file()
    
    def configure_root(self):
        self.root.option_add('*tearOff', FALSE)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def select_month(self, *args):
        global MONTHS
        idxs = self.list_box.curselection()

        if len(idxs)==1:
            index = int(idxs[0])
            self.list_box.see(index)
            self.display_month.set(f"Selectd month: {MONTHS[index]}")
            self.current_month = MONTHS[index]
            self.update_costs_label()
            self.udpate_gains_label()

    def update_costs_label(self):
        #UPDATED
        self.display_costs.set("Costs: " + str(self.data.get_total_costs(self.current_month)))

    def udpate_gains_label(self):
        #UPDATED
        self.display_gain.set("Gains: " + str(self.data.get_total_gains(self.current_month)))

    def update_costs(self, month_name, value, name = "", toDel = False):
        #UPDATED
        if toDel:
            self.data.delete_cost(month_name, name)
        else:
            self.data.add_cost(month_name, name, value)
        self.update_costs_label()
        return

    def show_costs(self, *args):
        #UPDATED
        tmp_month = ""
        indxs = self.list_box.curselection()
        if len(indxs) == 1:
            index = int(indxs[0])
            tmp_month = MONTHS[index]
            if tmp_month in self.open_windows_costs:
                if self.open_windows_costs[tmp_month] != None:
                    if self.open_windows_costs[tmp_month].get_active_window() == False:
                        self.open_windows_costs[tmp_month].open_window()
                else:
                    return
            else:
                self.open_windows_costs[tmp_month] = CostsWindow(self.root, tmp_month, self.update_costs, self.data.costs)

    def update_gains(self, month_name, value, name = "", toDel = False):
        #UPDATED
        if toDel:
            self.data.delete_gains(month_name, name)
        else:
            self.data.add_gains(month_name, name, value)
        self.udpate_gains_label()
        return
    
    def show_gains(self, *args):
        #UPDATED
        tmp_month = ""
        indxs = self.list_box.curselection()
        if len(indxs) == 1:
            index = int(indxs[0])
            tmp_month = MONTHS[index]
            if tmp_month in self.open_windows_gains:
                if self.open_windows_gains[tmp_month] != None:
                    if self.open_windows_gains[tmp_month].get_active_window() == False:
                        self.open_windows_gains[tmp_month].open_window()
                else:
                    return
            else:
                self.open_windows_gains[tmp_month] = GainsWindow(self.root, tmp_month, self.update_gains, self.data.gains)

    def initialize(self):
        global MONTHS
        #List box of months
        self.list_box = Listbox(self.content, height=5)
        for i in range(len(MONTHS)):
            self.list_box.insert(i, MONTHS[i])
        self.list_box.grid(column=0,row=0, sticky=(N, W, E, S))

        #Scroll for list box
        scrollbar = Scrollbar(self.content, orient=VERTICAL, command=self.list_box.yview)
        scrollbar.grid(column=1, row=0, sticky=(N, S))
        #list_box.configure(yscrollcommand=scrollbar.set)
        self.list_box['yscrollcommand'] = scrollbar.set
        self.list_box.bind('<<ListboxSelect>>', self.select_month)

        #Labels to show sleected month info
        l_selected = ttk.Label(self.content, textvariable=self.display_month)
        l_costs = ttk.Label(self.content, textvariable=self.display_costs)
        l_gain = ttk.Label(self.content, textvariable=self.display_gain)

        #Buttons
        costs_button = ttk.Button(self.content, text="Add costs", default="normal", command=self.show_costs)
        gains_button = ttk.Button(self.content, text="Add gains", default="normal", command=self.show_gains)
        #Positions
        l_selected.grid(column=0, row=1,sticky=(N,W))
        l_costs.grid(column=0, row=2, sticky=(N,W))
        l_gain.grid(column=0, row=3, sticky=(N,W))

        costs_button.grid(column=2, row=0, sticky=N)
        gains_button.grid(column=3, row=0, sticky=N)

        self.list_box.select_set(0)
        self.select_month()
    
    def save_to_file(self):
        with open("data.txt", "w") as file:
            file.write("D")
        pass

    def main(self):
        self.root.mainloop()


program = MainProgram()

program.main()