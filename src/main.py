import tkinter as tk
from tkinter import scrolledtext


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TODOList")
        self.geometry("800x500")
        self.resizable(width=0, height=0)
        
        self.draw()
    
    def draw(self):
        self._make_menu_bar()
        self._make_add_tab_button()

    def _make_menu_bar(self):
        # menu bar
        self.menubar = tk.Menu(self)

        # file menu in menu bar
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.donothing)
        self.filemenu.add_command(label="Open", command=self.donothing)
        self.filemenu.add_command(label="Save", command=self.donothing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # help menu
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help Index", command=self.donothing)
        self.helpmenu.add_command(label="About...", command=self.donothing)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.config(menu=self.menubar)

    def _make_add_tab_button(self):
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.grid(row=0, column=0, sticky="we")

        self.btn_tab = tk.Button(self.buttons_frame, text="Add Tab", command=self.add_new_tab)
        self.btn_tab.grid(row=0, column=0, padx=(10), pady=10)

        self.tab_name = tk.Text(self, height=1, width=20)
        self.tab_name.grid(row=0, column=1, sticky="we")

    def add_new_tab(self):
        input = self.tab_name.get("1.0", "end-1c")

        self.group1 = tk.LabelFrame(self, text=input, padx=5, pady=5)
        self.group1.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="sewn")

        self.columnconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)

        self.group1.rowconfigure(0, weight=1)
        self.group1.columnconfigure(0, weight=1)

        # Create the textbox
        self.txtbox = scrolledtext.ScrolledText(self.group1, width=40, height=10)
        self.txtbox.grid(row=0, column=0, sticky="sewn")

    def donothing(self):
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
