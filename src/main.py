from tkinter import *
from tkinter import ttk
root = Tk()
root.option_add('*tearOff', FALSE)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

content = ttk.Frame(root, padding=(10, 10 , 10, 10))
content.grid(column=0, row=0)

current_month = StringVar(value="Month:")
current_costs = StringVar(value="Costs:")
current_gain = StringVar(value="Gain:")

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

costs_dict = {"January": {
    "Kompen" : 12.0,
    "wokmm" : 1.0
}}
gains_dict = {}
open_costs = {}
open_gains = {}

class Window():
    def __init__(self, root, month):
        self.root = root
        self.month = month
        self.window = None
        self.open_window()
    
    def on_exit(self):
        if self.window:
            self.window.destroy()
        self.window = None
    
    def open_window(self):
        self.window = Toplevel(root)
        self.window.title(f"Costs of {self.month}")
        self.window.geometry("300x200")
        self.window.protocol("W_DELETE_WINDOW", self.on_exit)
    
    def get_active_window(self):
        if self.window is None and self.window.winfo_exists():
            return False
        return True


class CostsWindow(Window):
    def __init__(self, root, month):
        self.list_box = None
        self.cost_name = StringVar()
        self.cost_value = StringVar()
        super().__init__(root, month)
    
    def on_exit(self):
        super().on_exit()
        self.list_box = None

    def open_window(self):
        super().open_window()
        #Filling costs list
        global costs_dict
        self.list_box = Listbox(self.window, height=5)
        print(f"Self 1: {self}")
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
    
    def delete_element(self, *args):
        if self.list_box == None:
            return
        indxs = self.list_box.curselection()
        for index in indxs:
            self.list_box.delete(index, index)

    def add_element(self):
        if self.list_box == None:
            return
        if self.cost_name.get() != "" and self.cost_value.get() != "":
            self.list_box.insert(self.list_box.size(), str(self.cost_name.get() + " => " + self.cost_value.get()))
            self.cost_name.set("")
            self.cost_value.set("")
        else:
            return


def select_month(*args):
    global list_box
    idxs = list_box.curselection()
    if len(idxs)==1:
        index = int(idxs[0])
        print(index)
        list_box.see(index)
        current_month.set(f"Selectd month: {MONTHS[index]}")
        pass

def show_costs(*args):
    tmp_month = ""
    global list_box
    global root
    global open_costs
    indxs = list_box.curselection()
    if len(indxs) == 1:
        index = int(indxs[0])
        tmp_month = MONTHS[index]
        if tmp_month in open_costs:
            if open_costs[tmp_month] != None:
                print(open_costs)
                if open_costs[tmp_month].get_active_window() == False:
                    open_costs[tmp_month].open_window()
            else:
                return
        else:
            open_costs[tmp_month] = CostsWindow(root, tmp_month)
        
    

def show_gains(*args):
    pass

#List box of months
list_box = Listbox(content, height=5)
for i in range(len(MONTHS)):
    list_box.insert(i, MONTHS[i])
list_box.grid(column=0,row=0, sticky=(N, W, E, S))

#Scroll for list box
scrollbar = Scrollbar(content, orient=VERTICAL, command=list_box.yview)
scrollbar.grid(column=1, row=0, sticky=(N, S))
#list_box.configure(yscrollcommand=scrollbar.set)
list_box['yscrollcommand'] = scrollbar.set
list_box.bind('<<ListboxSelect>>', select_month)

#Labels to show sleected month info
l_selected = ttk.Label(content, textvariable=current_month)
l_costs = ttk.Label(content, textvariable=current_costs)
l_gain = ttk.Label(content, textvariable=current_gain)

#Buttons
costs_button = ttk.Button(content, text="Add costs", default="normal", command=show_costs)
gains_button = ttk.Button(content, text="Add gains", default="normal", command=show_gains)
#Positions
l_selected.grid(column=0, row=1,sticky=(N,W))
l_costs.grid(column=0, row=2, sticky=(N,W))
l_gain.grid(column=0, row=3, sticky=(N,W))

costs_button.grid(column=2, row=0, sticky=N)
gains_button.grid(column=3, row=0, sticky=N)

list_box.select_set(0)
select_month()

root.mainloop()