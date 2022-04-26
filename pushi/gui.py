import tkinter as tk
from tkinter import Tk, Frame, Label, Entry, ttk

"""
open up `pygubu-designer.exe to edit gui`
"""


class Gui:
    def __init__(self, master=None):
        self.win = tk.Tk() if master is None else tk.Toplevel(master)

        # string vars for user input
        self.cmd_entry_var = tk.StringVar()

        self.base = ttk.Frame(self.win)
        self.cmd_frame = ttk.Frame(self.base)
        self.cmd_label = ttk.Label(self.cmd_frame)
        self.cmd_label.configure(anchor=tk.N, font='TkDefaultFont', text='commands')
        self.cmd_label.pack(ipadx=5, pady=5, side=tk.LEFT)
        self.cmd_entry = ttk.Entry(self.cmd_frame, textvariable=self.cmd_entry_var)
        self.cmd_entry.pack(expand=True, fill=tk.X, ipadx=5, padx=5, pady=5, side=tk.LEFT)
        self.send_btn = ttk.Button(self.cmd_frame)
        self.send_btn.configure(state=tk.DISABLED, text='send')
        self.send_btn.pack(ipadx=5, padx=5, pady=5, side=tk.LEFT)
        self.cmd_frame.pack(anchor=tk.SW, expand=True, fill=tk.BOTH, side=tk.TOP)
        self.response_frame = ttk.Frame(self.base)
        self.the_console = tk.Text(self.response_frame)
        self.the_console.configure(background='#000000', foreground='#00ff00', highlightbackground='#00ff00',
                                   highlightcolor='#000000')
        self.the_console.pack(anchor=tk.NW, fill=tk.X, ipadx=5, ipady=5, padx=5, pady=5, side=tk.TOP)
        self.response_frame.configure(height=250)
        self.response_frame.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
        self.response_frame.pack_propagate(0)
        self.db_frame = ttk.Frame(self.base)
        self.db_tree = ttk.Treeview(self.db_frame)
        self.db_tree.pack(expand=True, fill=tk.BOTH, padx=5, side=tk.LEFT)
        self.db_tree_scroll = ttk.Scrollbar(self.db_frame)
        self.db_tree_scroll.configure(orient=tk.VERTICAL)
        self.db_tree_scroll.pack(fill=tk.Y, side=tk.LEFT)
        self.db_frame.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
        self.base.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
        self.win.configure(height=480, width=640)
        self.win.geometry('640x480')
        self.win.title('bitpushi')
        self.win.pack_propagate(0)

        self.bootstrap()

    def bootstrap(self):
        self.cmd_entry.bind('<KeyRelease>', self.cmd_entry_callback)

    def cmd_entry_callback(self, event):
        print(self.cmd_entry_var.get())

    def run(self):
        self.win.mainloop()


def boot_up():
    app = Gui()
    app.run()
