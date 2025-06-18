import tkinter as tk


class App(tk.Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)
        
        self.draw()
    
    def draw():
        pass


if __name__ == "__main__":
    pass
