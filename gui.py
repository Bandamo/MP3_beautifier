import tkinter.filedialog as filedialog
import tkinter as tk
import main
import random

class GUI(tk.Tk):
    def __init__(self, name : str, width = 500, height = 500):
        super().__init__(className=name)
        self.width = width
        self.height = height
        self.change_geometry()
        self.create_menu_bar()
        self.canvas = tk.Canvas(self,width=int(self.width/2),height=int(self.height/2))
        self.canvas.pack()
        self.output = tk.Text(self, width=50, height=10)
        self.output.pack()
    
    def create_menu_bar(self):
        menu_bar = tk.Menu(self)

        menu_menu = tk.Menu(menu_bar, tearoff=0)
        menu_menu.add_command(label="Choisir le dossier", command=self.choose_folder)
        menu_menu.add_command(label="Options", command=self.open_option)
        menu_menu.add_separator()
        menu_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="Menu", menu=menu_menu)

        menu_run = tk.Menu(menu_bar, tearoff=0)
        menu_run.add_command(label="Lancer", command=self.run)
        menu_run.add_command(label="Reprendre", command=self.print_random_number)
        menu_run.add_command(label="Stop", command=self.print_random_number)
        menu_bar.add_cascade(label="Lancer", menu=menu_run)

        self.config(menu=menu_bar)

    def choose_folder(self):
        filepath = filedialog.askdirectory()
        print(filepath)
    
    def run(self):
        main.main(self,True,True)

    def print_random_number(self):
        r = random.randint(0,100)
        self.output.insert(tk.END,str(r)+"\n")
        self.output.see("end")
        print(r)
    def open_option(self):
        preferences = options("Options", int(self.width/2), int(self.height/2))
    def change_geometry(self,width = None, height = None):
        if width != None:
            self.width = width
        if height != None:
            self.height = height
        
        textwh = str(self.width) + "x" + str(self.height)
        self.geometry(textwh)

class options(tk.Tk):
    def __init__(self, name : str, width = 500, height = 500):
        super().__init__(className=name)
        self.width = width
        self.height = height

if __name__=="__main__":
    gui = GUI(" MP3-Beautifier ")
    # set window size
    gui.mainloop() 