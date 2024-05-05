import tkinter as tk
from shapes_and_drawn_object import DrawnObject
from toolbar import *

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
        if None in obj or None in box:
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