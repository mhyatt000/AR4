import tkinter.ttk as ttk
import tkinter as tk


def build_components(parent):
    """docstring"""

    components = {}

    header = ttk.Frame(parent)
    header.grid(row=0, column=0, columnspan=3, pady=10, sticky='')
    components['header'] = header

    left = ttk.Frame(parent)
    left.grid(row=1, column=0, padx=10, sticky='')
    components['left'] = left
    mid = ttk.Frame(parent)
    mid.grid(row=1, column=1, padx=10, sticky='')
    components['mid'] = mid
    right = ttk.Frame(parent)
    right.grid(row=1, column=2, padx=10, sticky='')
    components['right'] = right

    footer = ttk.Frame(parent)
    footer.grid(row=2, column=0, columnspan=3, pady=10, sticky='')
    components['footer'] = footer

    center(parent)
    return components 

def center(parent):
    rows, columns = parent.grid_size()
    for i in range(columns):
        parent.grid_columnconfigure(i, weight=1) 
    for i in range(rows):
        parent.grid_rowconfigure(i, weight=1)  


def vgrid(parent, depth=1, **kwargs):
    for i, widget in enumerate(parent.winfo_children()):
        widget.grid(row=i // depth, column=i % depth, sticky='', **kwargs)
    center(parent)


def hgrid(parent, depth=1, **kwargs):
    for i, widget in enumerate(parent.winfo_children()):
        widget.grid(row=i % depth, column=i // depth, sticky='', **kwargs)
    center(parent)


def display(entry, value=""):
    """delete entry contents and insert value"""

    entry.delete(0, "end")
    entry.insert(0, value)

