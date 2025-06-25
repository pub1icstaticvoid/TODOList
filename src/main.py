import tkinter as tk
import json
from tkinter import scrolledtext, simpledialog
from pathlib import Path


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")
        # self.resizable(width=0, height=0)
        self.planners_json = "planners/planners.json"
        self.current_planner_name = ""
        self.tab_frames = []
        self.num_tabs = 1

        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, sticky="ns")

        self.tab_container = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.tab_container, anchor="nw")

        self.tab_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # checks if planners folder exists
        # if not, assume no planner files exists
        self.planners_path = Path("planners")
        if not self.planners_path.exists() or not Path(self.planners_json).exists():
            self.create_planners_folder()
            with open("planners/last_used.txt", "w") as f:
                f.write(self.current_planner_name)
        else:
            with open("planners/last_used.txt", "r") as f:
                self.current_planner_name = f.read()

        self.title("TODOList - " + self.current_planner_name)

        self.draw()
        self.load_planner()
        self.auto_save()

    def create_planners_folder(self):
        self.planners_path.mkdir(parents=True, exist_ok=True)
        self.withdraw()

        with open(self.planners_json, "w") as f:
            json.dump({}, f)

        while not self.current_planner_name:
            self.current_planner_name = self.create_new_planner()

        new_planner_data = {self.current_planner_name : {"tabs" : [], "notes" : []}}
        self.add_new_planner(new_planner_data)

        self.deiconify()

    def add_new_planner(self, new_data: dict):
        f = open(self.planners_json, "r")
        old_data = json.load(f)
        old_data.update(new_data)
        f.close()

        with open(self.planners_json, "w") as f:
            json.dump(old_data, f, indent=4)

    def create_new_planner(self):
        planner_name = simpledialog.askstring("TODOList", "Enter name for planner")
        
        return planner_name      

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

        self.btn_tab = tk.Button(self.buttons_frame, text="Add Tab", command=self.get_tab_name)
        self.btn_tab.grid(row=0, column=0, padx=(10), pady=10)

        self.tab_name = tk.Text(self, height=1, width=20)
        # self.tab_name.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        self.tab_name.place(x=110, y=23)

    def get_tab_name(self):
        input = self.tab_name.get("1.0", "end-1c").strip()

        with open(self.planners_json, "r") as f:
            data = json.load(f)
            data[self.current_planner_name]["tabs"].append(input)
            data[self.current_planner_name]["notes"].append("")
        self.save_planner()

        self.add_new_tab(input)

    def add_new_tab(self, input, notes=""):
        # dynamically creates new tab frame
        tab_frame = tk.LabelFrame(self.tab_container, text=input, padx=5, pady=5)
        tab_frame.grid(row=self.num_tabs, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        delete_tab_btn = tk.Button(tab_frame, text="X", command=lambda f=tab_frame: self.delete_tab(f))
        delete_tab_btn.grid(row=0, column=0, sticky="w")

        # Create the textbox
        txtbox = scrolledtext.ScrolledText(tab_frame, width=40, height=10)
        txtbox.grid(row=0, column=1, sticky="w", padx=10)
        txtbox.insert(tk.INSERT, notes)

        # clears tab name text box
        self.tab_name.delete("1.0", tk.END)
        # stores tab frame
        self.tab_frames.append(tab_frame)
        self.num_tabs += 1

    def delete_tab(self, tab_frame: tk.LabelFrame):
        with open(self.planners_json, "r") as f:
            data = json.load(f)
            tabs = data.get(self.current_planner_name, {}).get("tabs", [])
            notes = data.get(self.current_planner_name, {}).get("notes", [])

        tab_name = tab_frame.cget("text")

        txtbox = None
        children = tab_frame.winfo_children()
        if len(children) > 1:
            tab_content_frame = children[1]
            txtbox = None

            for child in tab_content_frame.winfo_children():
                if isinstance(child, scrolledtext.ScrolledText):
                    txtbox = child
                    break

        tab_text = txtbox.get("1.0", "end-1c") if txtbox else ""

        if tab_name in tabs:
            index = tabs.index(tab_name)
            tabs.pop(index)
            notes.pop(index)

        data[self.current_planner_name] = {
            "tabs" : tabs,
            "notes" : notes
        }
        
        self.save_planner()
        self.tab_frames.remove(tab_frame)
        tab_frame.destroy()

        if len(self.tab_frames) == 0:
            self.num_tabs = 1

    def save_planner(self):
        data = {}
        with open(self.planners_json, "r") as f:
            data = json.load(f)
        tabs = []
        notes = []

        for tab_frame in self.tab_frames:
            tabs.append(tab_frame.cget("text"))

            children = tab_frame.winfo_children()
            if len(children) > 1:
                tab_content_frame = children[1]
                txtbox = None

                for child in tab_content_frame.winfo_children():
                    if isinstance(child, scrolledtext.ScrolledText):
                        txtbox = child
                        break

            if txtbox:
                tab_text = txtbox.get("1.0", "end-1c")
                notes.append(tab_text)
            else:
                notes.append("")

        data[self.current_planner_name] = {
            "tabs" : tabs,
            "notes" : notes
        }

        with open(self.planners_json, "w") as f:
            json.dump(data, f, indent=4)

    def load_planner(self):
        with open(self.planners_json, "r") as f:
            data = json.load(f)
            planner_data = data.get(self.current_planner_name, {})
            tab_names = planner_data.get("tabs", [])
            tab_notes = planner_data.get("notes", [])

            for i, tab_name in enumerate(tab_names):
                self.add_new_tab(tab_name, tab_notes[i] if i < len(tab_notes) else "")

    def auto_save(self):
        self.save_planner()
        self.after(5000, self.auto_save)

    def donothing(self):
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
