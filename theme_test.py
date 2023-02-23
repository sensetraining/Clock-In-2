import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.minsize(600, 400)
x_cordinate = int((root.winfo_screenwidth() / 2) - 300)
y_cordinate = int((root.winfo_screenheight() / 2) - 200)
root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))

# Set the initial theme
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "light")

def change_theme():
    # NOTE: The theme's real name is azure-<mode>
    if root.tk.call("ttk::style", "theme", "use") == "azure-dark":
        # Set light theme
        root.tk.call("set_theme", "light")
    else:
        # Set dark theme
        root.tk.call("set_theme", "dark")

# Remember, you have to use ttk widgets
button = ttk.Button(text="Change theme!", command=change_theme)
button.pack()

input = ttk.Entry()
input.pack()

load = ttk.Progressbar(mode="determinate",length=400)
load.pack()

for i in range(7000):
    load['value'] += 0.01

root.mainloop()
