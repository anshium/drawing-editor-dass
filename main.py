import tkinter as tk
import pickle
from tkinter import filedialog


class Shape:
    def __init__(self, drawingSpace):
        self.drawingSpace = drawingSpace
        self.canvas = drawingSpace
        self.object = None
        self.selected = False
        self.drawn = False
        self.shape_name = ""
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.is_primitive = True

    def on_click(self, event):
        if not self.drawn:
            self.x1 = event.x
            self.y1 = event.y

    def on_drag(self, event):
        if not self.drawn:
            self.draw_shape(event)

    def on_release(self, event=None):
        if not self.drawn:
            self.drawn = True
            if self.x1 > self.x2:
                self.x1, self.x2 = self.x1, self.x2
            if self.y1 > self.y2:
                self.y1, self.y2 = self.y1, self.y2

            drawn_obj = DrawnObject(self.drawingSpace)
            drawn_obj.add_object(self)
            self.drawingSpace.drawn_objects.append(drawn_obj)

        self.prev_x1, self.prev_y1, self.prev_x2, self.prev_y2 = (
            self.x1,
            self.y1,
            self.x2,
            self.y2,
        )
        self.canvas.bind("<Button-1>", self.drawingSpace.on_click)
        self.canvas.bind("<B1-Motion>", self.drawingSpace.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.drawingSpace.on_release)

    def delete(self):
        self.canvas.delete(self.object)

    def move_on_click(self, event):
        self.x, self.y = event.x, event.y

    def move_on_drag(self, event, dx, dy):
        if self.corner_style == "Square":
            self.canvas.coords(
                self.object, self.x1 + dx, self.y1 + dy, self.x2 + dx, self.y2 + dy
            )
        if self.corner_style == "Rounded":
            if self.object:
                self.canvas.delete(self.object)
            self.object = self.round_rectangle(
                self.x1 + dx, self.y1 + dy, self.x2 + dx, self.y2 + dy
            )

    def update_coords(self, event, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy


class Rectangle(Shape):
    def __init__(self, drawingSpace):
        super().__init__(drawingSpace)
        self.shape_name = "Rectangle"
        self.corner_style = "Square"
        self.color = "Black"
        self.x1 = None
        self.y1 = None

    def draw_shape(self, event=None):
        if self.object:
            self.canvas.delete(self.object)
        if event is not None:
            self.x2, self.y2 = event.x, event.y
        if self.corner_style == "Square":
            self.object = self.canvas.create_rectangle(
                self.x1, self.y1, self.x2, self.y2, outline=self.color
            )
        if self.corner_style == "Rounded":
            self.object = self.round_rectangle(self.x1, self.y1, self.x2, self.y2)

    def duplicate(self):
        duplicate = Rectangle(self.drawingSpace)
        duplicate.x1, duplicate.y1, duplicate.x2, duplicate.y2 = (
            self.x1 + 20,
            self.y1 + 20,
            self.x2 + 20,
            self.y2 + 20,
        )
        duplicate.draw_shape()
        duplicate.drawn = True
        duplicate.canvas.bind("<Button-1>", duplicate.drawingSpace.on_click)
        duplicate.canvas.bind("<B1-Motion>", duplicate.drawingSpace.on_drag)
        duplicate.canvas.bind("<ButtonRelease-1>", duplicate.drawingSpace.on_release)
        return duplicate

    def round_rectangle(self, x1, y1, x2, y2, radius=25):
        points = [
            x1 + radius,
            y1,
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]
        return self.canvas.create_polygon(
            points, smooth=True, outline=self.color, fill=""
        )

    def apply_edits(self):
        self.canvas.delete(self.object)
        if self.corner_style == "Rounded":
            self.object = self.round_rectangle(self.x1, self.y1, self.x2, self.y2)
        if self.corner_style == "Square":
            self.object = self.canvas.create_rectangle(
                self.x1, self.y1, self.x2, self.y2, outline=self.color
            )

    def edit(self, master):
        col_dropdown = tk.StringVar(master)
        col_dropdown.set(self.color)
        corner_dropdown = tk.StringVar(master)
        corner_dropdown.set(self.corner_style)

        def color_selected(event):
            self.color = col_dropdown.get()

        def corner_selected(event):
            self.corner_style = corner_dropdown.get()

        col_options = ["Black", "Red", "Green", "Blue"]
        col_dropdown_menu = tk.OptionMenu(
            master, col_dropdown, *col_options, command=color_selected
        )
        tk.Label(master, text="Color").pack(fill=tk.X)
        col_dropdown_menu.pack(fill=tk.X)

        corner_options = ["Square", "Rounded"]
        corner_dropdown_menu = tk.OptionMenu(
            master, corner_dropdown, *corner_options, command=corner_selected
        )
        tk.Label(master, text="Border").pack(fill=tk.X)
        corner_dropdown_menu.pack(fill=tk.X)

        submit_button = tk.Button(master, text="Apply", command=self.apply_edits)
        submit_button.pack(fill=tk.X)


class Line(Shape):
    def __init__(self, drawingSpace):
        super().__init__(drawingSpace)
        self.shape_name = "Line"
        self.color = "Black"
        self.corner_style = "Square"
        self.x1 = None
        self.y1 = None

    def draw_shape(self, event=None):
        if self.object:
            self.canvas.delete(self.object)
        if event is not None:
            self.x2, self.y2 = event.x, event.y
        self.object = self.canvas.create_line(
            self.x1, self.y1, self.x2, self.y2, fill=self.color
        )

    def duplicate(self):
        duplicate = Line(self.drawingSpace)
        duplicate.x1, duplicate.y1, duplicate.x2, duplicate.y2 = (
            self.x1 + 20,
            self.y1 + 20,
            self.x2 + 20,
            self.y2 + 20,
        )
        duplicate.draw_shape()
        duplicate.drawn = True
        duplicate.canvas.bind("<Button-1>", duplicate.drawingSpace.on_click)
        duplicate.canvas.bind("<B1-Motion>", duplicate.drawingSpace.on_drag)
        duplicate.canvas.bind("<ButtonRelease-1>", duplicate.drawingSpace.on_release)
        return duplicate

    def apply_edits(self):
        self.canvas.itemconfig(self.object, fill=self.color, dash=())

    def edit(self, master):
        col_dropdown = tk.StringVar(master)
        col_dropdown.set(self.color)

        def color_selected(event):
            self.color = col_dropdown.get()

        col_options = ["Black", "Red", "Green", "Blue"]
        tk.Label(master, text="Color").pack(fill=tk.X)
        col_dropdown_menu = tk.OptionMenu(
            master, col_dropdown, *col_options, command=color_selected
        )
        col_dropdown_menu.pack(fill=tk.X)

        submit_button = tk.Button(master, text="Apply", command=self.apply_edits)
        submit_button.pack()


class DrawnObject:
    def __init__(self, drawingSpace):
        self.drawingSpace = drawingSpace
        self.is_primitive = False
        self.object_count = 0
        self.objects = []
        self.allowMove = False
        self.x1, self.y1, self.x2, self.y2 = None, None, None, None
        self.cursor_backup = self.drawingSpace.cget("cursor")

    def add_object(self, object):
        self.objects.append(object)
        self.object_count += 1
        self.x1 = min([min(obj.x1, obj.x2) for obj in self.objects])
        self.y1 = min([min(obj.y1, obj.y2) for obj in self.objects])
        self.x2 = max([max(obj.x1, obj.x2) for obj in self.objects])
        self.y2 = max([max(obj.y1, obj.y2) for obj in self.objects])

    def remove_object(self, object):
        self.objects.remove(object)
        self.object_count -= 1
        if self.object_count == 0:
            return
        self.x1 = min([min(obj.x1, obj.x2) for obj in self.objects])
        self.y1 = min([min(obj.y1, obj.y2) for obj in self.objects])
        self.x2 = max([max(obj.x1, obj.x2) for obj in self.objects])
        self.y2 = max([max(obj.y1, obj.y2) for obj in self.objects])

    def select(self):
        for obj in self.objects:
            if obj.is_primitive:
                if obj.shape_name == "Rectangle":
                    obj.canvas.itemconfig(obj.object, outline="#0096FF", dash=(6, 2))
                if obj.shape_name == "Line":
                    obj.canvas.itemconfig(obj.object, fill="#0096FF", dash=(6, 2))
            else:
                obj.select()

    def deselect(self):
        for obj in self.objects:
            if obj.is_primitive:
                if obj.shape_name == "Rectangle":
                    obj.canvas.itemconfig(obj.object, outline=obj.color, dash=())
                if obj.shape_name == "Line":
                    obj.canvas.itemconfig(obj.object, fill=obj.color, dash=())
            else:
                obj.deselect()

    def ungroup_once(self):
        new_obj = self.objects[-1]
        self.remove_object(new_obj)
        self.drawingSpace.drawn_objects.append(new_obj)

    def ungroup(self):
        if self.object_count == 1:
            return
        else:
            for obj in self.objects:
                if obj.object_count == 1:
                    self.drawingSpace.drawn_objects.append(obj)
                else:
                    obj.ungroup()
            if self in self.drawingSpace.drawn_objects:
                self.drawingSpace.drawn_objects.remove(self)

    def delete(self):
        if self.object_count == 1:
            self.objects[0].delete()
        else:
            for obj in self.objects:
                obj.delete()
        if self in self.drawingSpace.drawn_objects:
            self.drawingSpace.drawn_objects.remove(self)

    def duplicate(self):
        new_obj = DrawnObject(self.drawingSpace)
        for obj in self.objects:
            new_obj.add_object(obj.duplicate())
        return new_obj

    def copy(self):
        new_obj = self.duplicate()
        self.drawingSpace.drawn_objects.append(new_obj)

    def move_on_click(self, event):
        self.x, self.y = event.x, event.y
        for obj in self.objects:
            obj.move_on_click(event)

    def move_on_drag(self, event, dx=0, dy=0):
        for obj in self.objects:
            obj.move_on_drag(event, event.x - self.x, event.y - self.y)

    def update_coords(self, event, dx=0, dy=0):
        self.allowMove = False
        self.drawingSpace.config(cursor=self.cursor_backup)
        self.drawingSpace.bind("<Button-1>", self.drawingSpace.on_click)
        self.drawingSpace.bind("<B1-Motion>", self.drawingSpace.on_drag)
        self.drawingSpace.bind("<ButtonRelease-1>", self.drawingSpace.on_release)
        dx, dy = event.x - self.x, event.y - self.y
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
        for obj in self.objects:
            obj.update_coords(event, dx, dy)

    def move(self):
        if not self.allowMove:
            self.allowMove = True
            self.cursor_backup = self.drawingSpace.cget("cursor")
            self.drawingSpace.config(cursor="fleur")
            self.drawingSpace.bind("<Button-1>", self.move_on_click)
            self.drawingSpace.bind("<B1-Motion>", self.move_on_drag)
            self.drawingSpace.bind("<ButtonRelease-1>", self.update_coords)
        else:
            self.allowMove = False
            self.drawingSpace.config(cursor=self.cursor_backup)
            self.drawingSpace.bind("<Button-1>", self.drawingSpace.on_click)
            self.drawingSpace.bind("<B1-Motion>", self.drawingSpace.on_drag)
            self.drawingSpace.bind("<ButtonRelease-1>", self.drawingSpace.on_release)


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


class DrawingSpace(tk.Canvas):
    def __init__(self, master, app, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.app = app
        self.selected_objects = []
        self.drawn_objects = []
        self.selectedToolbar = None

        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonPress-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)

        self.select_rect = None
        self.x1_select, self.y1_select, self.x2_select, self.y2_select = (
            None,
            None,
            None,
            None,
        )

    def on_click(self, event=None):
        for drawn_obj in self.drawn_objects:
            drawn_obj.deselect()
        if self.selectedToolbar is not None:
            self.selectedToolbar.destroy()
        self.selected_objects = []
        if event is not None:
            self.x1_select, self.y1_select = event.x, event.y

    def on_drag(self, event):
        if self.select_rect:
            self.delete(self.select_rect)
        self.x2_select, self.y2_select = event.x, event.y
        self.select_rect = self.create_rectangle(
            self.x1_select,
            self.y1_select,
            self.x2_select,
            self.y2_select,
            outline="#0096FF",
        )

    def on_release(self, event):
        self.delete(self.select_rect)
        for obj in self.drawn_objects:
            if self.inside_rect(
                [obj.x1, obj.y1, obj.x2, obj.y2],
                [self.x1_select, self.y1_select, self.x2_select, self.y2_select],
            ):
                obj.select()
                self.selected_objects.append(obj)
        print(f"Selected objects: {[obj for obj in self.selected_objects]}")
        self.draw_toolbar()

    def inside_rect(self, obj, box):
        if box[2] is None or box[3] is None:
            return False
        if (
            min(obj[0], obj[2]) >= min(box[0], box[2])
            and max(obj[0], obj[2]) <= max(box[0], box[2])
            and min(obj[1], obj[3]) >= min(box[1], box[3])
            and max(obj[1], obj[3]) <= max(box[1], box[3])
        ):
            return True
        return False

    def draw_toolbar(self):
        if (
            len(self.selected_objects) == 1
            and self.selected_objects[0].object_count == 1
        ):
            self.selectedToolbar = ShapeToolbar(
                self.app.toolbar, self.app, width=150, height=500
            )
            self.selectedToolbar.pack(fill=tk.X)
        if (
            len(self.selected_objects) == 1
            and self.selected_objects[0].object_count > 1
        ):
            self.selectedToolbar = GroupToolbar(
                self.app.toolbar, self.app, width=150, height=500
            )
            self.selectedToolbar.pack(fill=tk.X)
        if len(self.selected_objects) > 1:
            self.selectedToolbar = SelectionToolbar(
                self.app.toolbar, self.app, width=150, height=500
            )
            self.selectedToolbar.pack(fill=tk.X)

    def resize_canvas(self, event):
        self.config(width=event.width, height=event.height)


class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Drawing Editor")
        self.master.geometry("800x600")

        self.canvas = DrawingSpace(master, self, bg="white", width=600, height=600)
        self.toolbar = Toolbar(self, master, self.canvas, width=150, height=600)

        self.toolbar.pack(side=tk.LEFT, fill=tk.Y)
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.master.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        self.canvas.resize_canvas(event)

    def save_drawing(self, filename):
        drawn_objects_info = []
        for drawn_obj in self.canvas.drawn_objects:
            obj_info = {
                "type": "group" if not drawn_obj.is_primitive else "primitive",
                "objects": [],
            }
            if not drawn_obj.objects[0].is_primitive:
                for obj in drawn_obj.objects:
                    obj_info["objects"].append(
                        {
                            "type": obj.shape_name,
                            "coordinates": [obj.x1, obj.y1, obj.x2, obj.y2],
                            "color": obj.color,
                        }
                    )
            else:
                obj = drawn_obj.objects[0]
                obj_info["objects"].append(
                    {
                        "type": obj.shape_name,
                        "coordinates": [obj.x1, obj.y1, obj.x2, obj.y2],
                        "color": obj.color,
                    }
                )
            drawn_objects_info.append(obj_info)

        with open(filename, "wb") as file:
            pickle.dump(drawn_objects_info, file)
        print("Drawing saved successfully.")

    def import_drawing(self, filename):
        with open(filename, "rb") as file:
            drawn_objects_info = pickle.load(file)
        if drawn_objects_info:
            # Clear Canvas
            self.canvas.delete("all")
            for obj_info in drawn_objects_info:
                if obj_info["type"] == "group":
                    drawn_obj = DrawnObject(self.canvas)
                    for obj_data in obj_info["objects"]:
                        shape_type = obj_data["type"]
                        coordinates = obj_data["coordinates"]
                        color = obj_data["color"]
                        if shape_type == "Rectangle":
                            obj = Rectangle(self.canvas)
                        elif shape_type == "Line":
                            obj = Line(self.canvas)
                        obj.x1, obj.y1, obj.x2, obj.y2 = coordinates
                        obj.color = color
                        obj.draw_shape()
                        obj.drawn = True
                        obj.on_release()
                        drawn_obj.add_object(obj)
                    self.canvas.drawn_objects.append(drawn_obj)
                elif obj_info["type"] == "primitive":
                    obj_data = obj_info["objects"][0]
                    shape_type = obj_data["type"]
                    coordinates = obj_data["coordinates"]
                    color = obj_data["color"]
                    if shape_type == "Rectangle":
                        obj = Rectangle(self.canvas)
                    elif shape_type == "Line":
                        obj = Line(self.canvas)
                    obj.x1, obj.y1, obj.x2, obj.y2 = coordinates
                    obj.color = color
                    obj.draw_shape()
                    obj.on_release()
                    # drawn_obj = DrawnObject(self.canvas)
                    # drawn_obj.add_object(obj)
                    # self.canvas.drawn_objects.append(drawn_obj)
            print("Drawing imported successfully.")


class FileHandler:
    @staticmethod
    def save_to_file(drawn_objects, filename):
        try:
            with open(filename, "wb") as file:
                pickle.dump(drawn_objects, file)
            print("Drawing saved successfully.")
        except Exception as e:
            print(f"Error saving drawing: {e}")

    @staticmethod
    def import_from_file(filename):
        try:
            with open(filename, "rb") as file:
                drawn_objects = pickle.load(file)
            print("Drawing imported successfully.")
            return drawn_objects
        except FileNotFoundError:
            print("File not found.")
            return None
        except Exception as e:
            print(f"Error importing drawing: {e}")
            return None


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
