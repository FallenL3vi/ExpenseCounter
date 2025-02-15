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

costs_dict = {}
gains_dict = {"January": {
    "Kompen" : 12.0,
    "wokmm" : 1.0
}}
open_costs = {}
open_gains = {}
months_data = {}

float_regex = r"^(?:[1-9]\d*(?:[.,]\d+)?|0?[.,]\d*[1-9]\d*|0)$"

class Window():
    def __init__(self, root, month):
        self.root = root
        self.month = month
        self.window = None
    
    def on_exit(self):
        if self.window:
            self.window.destroy()
        self.window = None
    
    def open_window(self):
        self.window = Toplevel(self.root)
        self.window.title(f"Costs of {self.month}")
        self.window.geometry("300x200")
        self.window.protocol("WM_DELETE_WINDOW", self.on_exit)
    
    def get_active_window(self):
        if self.window is None:# and self.window.winfo_exists():
            return False
        return True


class CostsWindow(Window):
    def __init__(self, root, month, callback):
        self.list_box = None
        self.cost_name = StringVar()
        self.cost_value = StringVar()
        self._callback = callback
        self.value = 0.0
        super().__init__(root, month)
        self.sum_value()
        self.open_window()
    
    def on_exit(self):
        super().on_exit()
        self.list_box = None

    def open_window(self):
        super().open_window()
        #Filling costs list
        global costs_dict
        self.list_box = Listbox(self.window, height=5)
        if self.month in costs_dict:
            index = 0
            for key in costs_dict[self.month].keys():
                self.list_box.insert(index, str(key + " => " + str(costs_dict[self.month][key])))
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
        self._callback(self.month, self.value)

    def sum_value(self):
        global costs_dict
        if not self.month in costs_dict:
            return
        values = costs_dict[self.month].values()
        sum = 0.0
        for value in values:
            sum += float(value)
        self.value = sum


    def delete_element(self, *args):
        global costs_dict
        if self.list_box == None:
            return
        indxs = self.list_box.curselection()
        for index in indxs:
            tmp_title = self.list_box.get(index, index)[0].split("=>")[0].rstrip()
            self.list_box.delete(index, index)
            if tmp_title:
                if self.month in costs_dict:
                    del(costs_dict[self.month][tmp_title])
        self.sum_value()
        self._callback(self.month, self.value)

    def add_element(self):
        global float_regex
        global costs_dict

        if self.list_box == None:
            return
        if self.cost_name.get() != "" and self.cost_value.get() != "":
            if not self.month in costs_dict:
                costs_dict[self.month] = {}

            if not re.match(float_regex, self.cost_value.get()):
                print(f"Regex failed regex: {float_regex} : value : {self.cost_value.get()}")
                #TO DO => add error message
                return
            if self.cost_name.get() in costs_dict[self.month]:
                print("Name exists in costs")
                #TO DO => add error message
                return
            self.list_box.insert(self.list_box.size(), str(self.cost_name.get() + " => " + self.cost_value.get()))

            try:
                costs_dict[self.month][self.cost_name.get()] = float(self.cost_value.get())
            except Exception as error:
                print(f"Error in casting string to float : {error}")
                return

            self.sum_value()
            self._callback(self.month, self.value)
            self.cost_name.set("")
            self.cost_value.set("")
        else:
            return


class GainsWindow(Window):
    def __init__(self, root, month, callback):
        self.list_box = None
        self.gain_name = StringVar()
        self.gain_value = StringVar()
        self._callback = callback
        self.value = 0.0
        super().__init__(root, month)
        self.sum_value()
        self.open_window()
    
    def on_exit(self):
        super().on_exit()
        self.list_box = None

    def open_window(self):
        super().open_window()
        #Filling gains list
        global gains_dict
        self.list_box = Listbox(self.window, height=5)
        if self.month in gains_dict:
            index = 0
            for key in gains_dict[self.month].keys():
                self.list_box.insert(index, str(key + " => " + str(gains_dict[self.month][key])))
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
        self._callback(self.month, self.value)
        
    
    def sum_value(self):
        global gains_dict
        if not self.month in gains_dict:
            return
        values = gains_dict[self.month].values()
        sum = 0.0
        for value in values:
            sum += float(value)
        self.value = sum


    def delete_element(self, *args):
        global gains_dict
        if self.list_box == None:
            return
        indxs = self.list_box.curselection()
        for index in indxs:
            tmp_title = self.list_box.get(index, index)[0].split("=>")[0].rstrip()
            self.list_box.delete(index, index)
            if tmp_title:
                if self.month in gains_dict:
                    del(gains_dict[self.month][tmp_title])
        self.sum_value()
        self._callback(self.month, self.value)

    def add_element(self):
        global float_regex
        global gains_dict

        if self.list_box == None:
            return
        if self.gain_name.get() != "" and self.gain_value.get() != "":
            if not self.month in gains_dict:
                gains_dict[self.month] = {}

            if not re.match(float_regex, self.gain_value.get()):
                print(f"Regex failed regex: {float_regex} : value : {self.gain_value.get()}")
                #TO DO => add error message
                return
            if self.gain_name.get() in gains_dict[self.month]:
                print("Name exists in gains")
                #TO DO => add error message
                return
            self.list_box.insert(self.list_box.size(), str(self.gain_name.get() + " => " + self.gain_value.get()))

            try:
                gains_dict[self.month][self.gain_name.get()] = float(self.gain_value.get())
            except Exception as error:
                print(f"Error in casting string to float : {error}")
                return

            self.sum_value()
            self._callback(self.month, self.value)
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
        global costs_dict
        idxs = self.list_box.curselection()

        if len(idxs)==1:
            index = int(idxs[0])
            #print(index)
            self.list_box.see(index)
            self.display_month.set(f"Selectd month: {MONTHS[index]}")
            self.current_month = MONTHS[index]
            self.update_costs_label()
            self.udpate_gains_label()

    def update_costs_label(self):
        if self.current_month in months_data:
            self.display_costs.set("Costs: " + str(months_data[self.current_month]["COSTS"]))
        else:
            self.display_costs.set("Costs: 0.0")

    def udpate_gains_label(self):
        if self.current_month in months_data:
            self.display_gain.set("Gains: " + str(months_data[self.current_month]["GAINS"]))
        else:
            self.display_gain.set("Gains: 0.0")

    def update_costs(self, month_name, value):
        if month_name in months_data:
            months_data[month_name]["COSTS"] = value
        self.update_costs_label()
        return

    def show_costs(self, *args):
        global open_costs

        tmp_month = ""
        indxs = self.list_box.curselection()
        if len(indxs) == 1:
            index = int(indxs[0])
            tmp_month = MONTHS[index]
            if tmp_month in open_costs:
                if open_costs[tmp_month] != None:
                    if open_costs[tmp_month].get_active_window() == False:
                        open_costs[tmp_month].open_window()
                else:
                    return
            else:
                open_costs[tmp_month] = CostsWindow(self.root, tmp_month, self.update_costs)

    def update_gains(self, month_name, value):
        if month_name in months_data:
            months_data[month_name]["GAINS"] = value
        self.udpate_gains_label()
        return
    
    def show_gains(self, *args):
        global open_gains

        tmp_month = ""
        indxs = self.list_box.curselection()
        if len(indxs) == 1:
            index = int(indxs[0])
            tmp_month = MONTHS[index]
            if tmp_month in open_gains:
                if open_gains[tmp_month] != None:
                    if open_gains[tmp_month].get_active_window() == False:
                        open_gains[tmp_month].open_window()
                else:
                    return
            else:
                open_gains[tmp_month] = GainsWindow(self.root, tmp_month, self.update_gains)

    def initialize(self):
        global MONTHS
        #Initalize months
        for month in MONTHS:
            months_data[month] = {"COSTS" : 0.0, "GAINS" : 0.0}
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