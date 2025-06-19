import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TODOList")
        self.geometry("600x400")
        
        self.file_path = "todolist.txt"
        
        self.draw()
    
    def draw(self):
        self.text_area = tk.Text(self, wrap='word', font=("Arial", 12))
        self.text_area.pack(expand=True, fill='both')

        button_frame = tk.Frame(self)
        button_frame.pack(fill='x')

        save_btn = tk.Button(button_frame, text="Save", command=self.save_notes)
        save_btn.pack(side='left', padx=5, pady=5)

        load_btn = tk.Button(button_frame, text="Load", command=self.load_notes)
        load_btn.pack(side='left', padx=5, pady=5)

    def save_notes(self):
        try:
            with open(self.file_path, 'w') as f:
                f.write(self.text_area.get("1.0", tk.END).strip())
            print("Saved", "Notes saved successfully!")
        except Exception as e:
            print("Error", str(e))

    def load_notes(self):
        try:
            with open(self.file_path, 'r') as f:
                content = f.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, content)
            print("Loaded", "Notes loaded successfully!")
        except FileNotFoundError:
            print("File Not Found", "No saved notes yet.")
        except Exception as e:
            print("Error", str(e))


if __name__ == "__main__":
    app = App()
    app.mainloop()
