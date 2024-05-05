import tkinter as tk
from shapes_and_drawn_object import *

class Toolbar(tk.Frame):
    def __init__(self, app, master, drawingSpace, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.drawingSpace = drawingSpace
        self.app = app
        self.pack_propagate(0)

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
        self.button_import = tk.Button(
            self, text="Import", command=self.import_drawing, width=10
        )

        self.button_line.pack(fill=tk.X)
        self.button_rectangle.pack(fill=tk.X)
        self.button_save.pack(fill=tk.X)
        self.button_import.pack(fill=tk.X)
        tk.Label(self, text="").pack(fill=tk.X)

    def draw_line(self):
        self.drawingSpace.on_click()
        Line(self.drawingSpace)

    def draw_rectangle(self):
        self.drawingSpace.on_click()
        Rectangle(self.drawingSpace)

    def save_drawing(self):
        filename = tk.filedialog.asksaveasfilename(defaultextension=".dat")
        if filename:
            self.app.save_drawing(filename)

    def import_drawing(self):
        filename = tk.filedialog.askopenfilename(defaultextension=".dat")
        if filename:
            self.app.import_drawing(filename)


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

    def copy_object(self):
        self.app.canvas.selected_objects[0].copy()

    def move_object(self):
        self.app.canvas.selected_objects[0].move()

    def edit_object(self):
        edit_frame = tk.Frame(self, pady=10, borderwidth=10, padx=10)
        edit_frame.pack(fill=tk.X)
        tk.Label(edit_frame, text="Edit Options", pady=10).pack(fill=tk.X)

        self.app.canvas.selected_objects[0].objects[0].edit(edit_frame)

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
        self.close()

    def ungroup_all(self):
        self.app.canvas.selected_objects[0].ungroup()
        self.close()

    def delete_group(self):
        self.app.canvas.selected_objects[0].delete()
        self.close()

    def copy_group(self):
        self.app.canvas.selected_objects[0].copy()

    def move_group(self):
        self.app.canvas.selected_objects[0].move()

    def close(self):
        self.destroy()
        self.app.canvas.on_click()