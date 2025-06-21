import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TODOList")
        self.geometry("800x500")
        self.resizable(width=0, height=0)
        
        self.draw()
    
    def draw(self):
        self._make_menu_bar()

    def _make_menu_bar(self):
        # menu bar
        self.menubar = tk.Menu(self)

        # file menu in menu bar
        filemenu = tk.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.donothing)
        filemenu.add_command(label="Open", command=self.donothing)
        filemenu.add_command(label="Save", command=self.donothing)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        # help menu
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help Index", command=self.donothing)
        self.helpmenu.add_command(label="About...", command=self.donothing)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.config(menu=self.menubar)


    def donothing(self):
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
