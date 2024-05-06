import tkinter as tk

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
        duplicate.color = self.color
        duplicate.corner_style = self.corner_style
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
        duplicate.color = self.color
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