import tkinter as tk
from tkinter import scrolledtext


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TODOList")
        self.geometry("800x500")
        # self.resizable(width=0, height=0)
        self.tab_frames = []
        
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
        self.buttons_frame.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.btn_tab = tk.Button(self.buttons_frame, text="Add Tab", command=self.add_new_tab)
        self.btn_tab.grid(row=0, column=0, padx=(10), pady=10)

        self.tab_name = tk.Text(self, height=1, width=20)
        # self.tab_name.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        self.tab_name.place(x=110, y=23)

    def add_new_tab(self):
        input = self.tab_name.get("1.0", "end-1c").strip()

        # dynamically creates new tab frame
        tab_frame = tk.LabelFrame(self, text=input, padx=5, pady=5)
        tab_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        delete_tab_btn = tk.Button(tab_frame, text="X", command=lambda f=tab_frame: self.delete_tab(f))
        delete_tab_btn.grid(row=0, column=0, sticky="w")

        # Create the textbox
        txtbox = scrolledtext.ScrolledText(tab_frame, width=40, height=10)
        txtbox.grid(row=0, column=1, sticky="w", padx=10)

        # clears tab name text box
        self.tab_name.delete("1.0", tk.END)
        # stores tab frame
        self.tab_frames.append(tab_frame)

    def delete_tab(self, tab_frame: tk.LabelFrame):
        tab_frame.destroy()
        self.tab_frames.remove(tab_frame)

    def donothing(self):
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
