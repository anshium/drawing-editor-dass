import tkinter as tk
from tkinter import filedialog
from shapes_and_drawn_object import *

class Toolbar(tk.Frame):
    def __init__(self, app, master, drawingSpace, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.drawingSpace = drawingSpace
        self.app = app
        self.pack_propagate(0)
        self.saved_once = False  # Track if the drawing has been saved at least once

        tk.Label(self, text="Draw Shapes", pady=10).pack(fill=tk.X)
        self.button_line = tk.Button(
            self, text="Line", command=self.draw_line, width=10
        )
        self.button_rectangle = tk.Button(
            self, text="Rectangle", command=self.draw_rectangle, width=10
        )
        self.button_save = tk.Button(
            self, text="Save", command=self.save_drawing, width=10
        )
        self.button_save_as = tk.Button(
            self, text="Save As", command=self.save_as_drawing, width=10
        )
        self.button_import = tk.Button(
            self, text="Import", command=self.import_drawing, width=10
        )

        self.button_line.pack(fill=tk.X)
        self.button_rectangle.pack(fill=tk.X)
        self.button_save.pack(fill=tk.X)
        self.button_save_as.pack(fill=tk.X)
        self.button_import.pack(fill=tk.X)
        tk.Label(self, text="").pack(fill=tk.X)

    def draw_line(self):
        self.drawingSpace.on_click()
        Line(self.drawingSpace)

    def draw_rectangle(self):
        self.drawingSpace.on_click()
        Rectangle(self.drawingSpace)

    def save_drawing(self):
		# If already saved once, just save
        if self.app.saved_once:
            filename = self.app.current_save_target_file
        else:  # If not saved yet, behave like "Save As"
            filename = tk.filedialog.asksaveasfilename(defaultextension=".dat")
            if filename:
                self.app.saved_once = True
                self.app.current_save_target_file = filename
        if filename:
            self.app.save_drawing(filename)

    def save_as_drawing(self):
        filename = tk.filedialog.asksaveasfilename(defaultextension=".dat")
        if filename:
            self.saved_once = True
            self.app.current_save_target_file = filename
            self.app.save_drawing(filename)

    def import_drawing(self):
        filename = tk.filedialog.askopenfilename(defaultextension=".dat")
        if filename:
            self.app.import_drawing(filename)
            self.app.current_save_target_file = filename
