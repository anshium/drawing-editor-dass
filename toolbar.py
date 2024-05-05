import tkinter as tk
from tkinter import filedialog
from shapes_and_drawn_object import *

from tkinter import messagebox

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
        self.button_export_xml = tk.Button(
            self, text="Export to XML", command=self.export_to_xml, width=10
        )
        self.button_import_xml = tk.Button(
            self, text="Import from XML", command=self.import_from_xml, width=10
        )

        self.button_line.pack(fill=tk.X)
        self.button_rectangle.pack(fill=tk.X)
        self.button_save.pack(fill=tk.X)
        self.button_save_as.pack(fill=tk.X)
        self.button_import.pack(fill=tk.X)
        self.button_export_xml.pack(fill=tk.X)
        self.button_import_xml.pack(fill=tk.X)
        tk.Label(self, text="").pack(fill=tk.X)

    def draw_line(self):
        self.drawingSpace.on_click()
        Line(self.drawingSpace)
        self.app.unsaved_changes = True

    def draw_rectangle(self):
        self.drawingSpace.on_click()
        Rectangle(self.drawingSpace)
        self.app.unsaved_changes = True

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
            self.app.unsaved_changes = False

    def save_as_drawing(self):
        filename = tk.filedialog.asksaveasfilename(defaultextension=".dat")
        if filename:
            self.saved_once = True
            self.app.current_save_target_file = filename
            self.app.save_drawing(filename)
            self.app.unsaved_changes = False

    def import_drawing(self):
        if self.app.unsaved_changes:
            response = messagebox.askyesnocancel(
				"Unsaved Changes",
				"There are unsaved changes. Do you want to save them before importing?",
			)
            if response == messagebox.YES:
                self.toolbar.save_drawing()
                self.app.unsaved_changes = False
            elif response == messagebox.CANCEL:
                pass

        filename = tk.filedialog.askopenfilename(defaultextension=".dat")
        if filename:
            self.app.import_drawing(filename)
            self.app.current_save_target_file = filename
            self.app.unsaved_changes = False
            
    def export_to_xml(self):
        filename = tk.filedialog.asksaveasfilename(defaultextension=".xml")
        if filename:
            self.app.export_to_xml(filename)
    
    def import_from_xml(self):
        filename = tk.filedialog.askopenfilename(defaultextension=".xml")
        if filename:
            self.app.import_from_xml(filename)

class ShapeToolbar(tk.Frame):
    def __init__(self, master, app, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.app = app
        self.pack_propagate(0)
        tk.Label(self, text="Shape Options", pady=10).pack(fill=tk.X)

        self.button_delete = tk.Button(
            self, text="Delete", command=self.delete_object, width=10
        )
        self.button_delete.pack(fill=tk.X)
        self.button_copy = tk.Button(
            self, text="Copy", command=self.copy_object, width=10
        )
        self.button_copy.pack(fill=tk.X)
        self.button_move = tk.Button(
            self, text="Move", command=self.move_object, width=10
        )
        self.button_move.pack(fill=tk.X)
        self.button_edit = tk.Button(
            self, text="Edit", command=self.edit_object, width=10
        )
        self.button_edit.pack(fill=tk.X)

    def delete_object(self):
        self.app.canvas.selected_objects[0].delete()
        self.close()
        self.app.unsaved_changes = True

    def copy_object(self):
        self.app.canvas.selected_objects[0].copy()
        self.app.unsaved_changes = True

    def move_object(self):
        self.app.canvas.selected_objects[0].move()
        self.app.unsaved_changes = True

    def edit_object(self):
        edit_frame = tk.Frame(self, pady=10, borderwidth=10, padx=10)
        edit_frame.pack(fill=tk.X)
        tk.Label(edit_frame, text="Edit Options", pady=10).pack(fill=tk.X)

        self.app.canvas.selected_objects[0].objects[0].edit(edit_frame)
        self.app.unsaved_changes = True

    def close(self):
        self.destroy()
        self.app.canvas.on_click()


class SelectionToolbar(tk.Frame):
    def __init__(self, master, app, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.app = app
        self.pack_propagate(0)
        tk.Label(self, text="Selection Options", pady=10).pack(fill=tk.X)

        self.button_group = tk.Button(
            self, text="Group", command=self.group_objects, width=10
        )
        self.button_group.pack(fill=tk.X)

    def group_objects(self):
        new_obj = DrawnObject(self.app.canvas)
        for obj in self.app.canvas.selected_objects:
            new_obj.add_object(obj)
            self.app.canvas.drawn_objects.remove(obj)
        self.app.canvas.drawn_objects.append(new_obj)
        
        self.app.unsaved_changes = True
        
        self.close()

    def close(self):
        self.destroy()
        self.app.canvas.on_click()


class GroupToolbar(tk.Frame):
    def __init__(self, master, app, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.app = app
        self.pack_propagate(0)
        tk.Label(self, text="Group Options", pady=10).pack(fill=tk.X)

        self.button_ungroup = tk.Button(
            self, text="Un-Group", command=self.ungroup_once, width=10
        )
        self.button_ungroup.pack(fill=tk.X)

        self.button_ungroup_all = tk.Button(
            self, text="Un-Group All", command=self.ungroup_all, width=10
        )
        self.button_ungroup_all.pack(fill=tk.X)

        self.button_delete = tk.Button(
            self, text="Delete", command=self.delete_group, width=10
        )
        self.button_delete.pack(fill=tk.X)
        self.button_copy = tk.Button(
            self, text="Copy", command=self.copy_group, width=10
        )
        self.button_copy.pack(fill=tk.X)
        self.button_move = tk.Button(
            self, text="Move", command=self.move_group, width=10
        )
        self.button_move.pack(fill=tk.X)

    def ungroup_once(self):
        self.app.canvas.selected_objects[0].ungroup_once()
        self.app.unsaved_changes = True
        self.close()

    def ungroup_all(self):
        self.app.canvas.selected_objects[0].ungroup()
        self.app.unsaved_changes = True
        self.close()

    def delete_group(self):
        self.app.canvas.selected_objects[0].delete()
        self.app.unsaved_changes = True
        self.close()

    def copy_group(self):
        self.app.canvas.selected_objects[0].copy()
        self.app.unsaved_changes = True

    def move_group(self):
        self.app.canvas.selected_objects[0].move()
        self.app.unsaved_changes = True

    def close(self):
        self.destroy()
        self.app.canvas.on_click()