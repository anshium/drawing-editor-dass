import tkinter as tk
import pickle
from tkinter import filedialog
from tkinter import messagebox

from shapes_and_drawn_object import Rectangle, Line
from shapes_and_drawn_object import DrawnObject
from DrawingSpace import DrawingSpace
from toolbar import Toolbar
from file_handler import FileHandler

import xml.etree.ElementTree as ET

import sys

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Drawing Editor")
        self.master.geometry("800x600")

        self.canvas = DrawingSpace(master, self, bg="white", width=600, height=600)
        self.toolbar = Toolbar(self, master, self.canvas, width=150, height=600)

        self.saved_once = False
        self.current_save_target_file = ""
        self.unsaved_changes = False

        self.toolbar.pack(side=tk.LEFT, fill=tk.Y)
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.master.bind("<Configure>", self.on_resize)
        
        self.master.protocol("WM_DELETE_WINDOW", self.handle_window_close)

    def on_resize(self, event):
        self.canvas.resize_canvas(event)

    def handle_window_close(self):
        if self.unsaved_changes:
            response = tk.messagebox.askyesno(
				"Unsaved Changes",
				"There are unsaved changes. Do you want to save them before closing the application?",
			)
            if response == True:
                self.toolbar.save_drawing()
                self.unsaved_changes = False
                print("Saved Changes!")
        self.master.destroy()

def main():
            
    
    root = tk.Tk()
    app = DrawingApp(root)
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            app.import_drawing(filename)
            app.current_save_target_file = filename
            app.saved_once = True
        except:
            print("Import not possible, Using this file to save data. Clearing existing data")
            with open(filename, 'w') as f:
                app.current_save_target_file = filename
                app.saved_once = True
    
    root.mainloop()
    
            


if __name__ == "__main__":
    main()
