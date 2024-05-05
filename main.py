import tkinter as tk
import pickle
from tkinter import filedialog

from shapes_and_drawn_object import Rectangle, Line
from shapes_and_drawn_object import DrawnObject
from DrawingSpace import DrawingSpace
from toolbar import Toolbar
from file_handler import FileHandler


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

    def to_append_routine(self, drawn_objects):
        append_list = []
        for drawn_obj in drawn_objects:
            if drawn_obj.objects[0].is_primitive:
                obj = drawn_obj.objects[0]
                if obj.shape_name == "Line":
                    append_list.append({
                        "type": obj.shape_name,
                        "coordinates": [obj.x1, obj.y1, obj.x2, obj.y2],
                        "color": obj.color
                    })
                elif obj.shape_name == "Rectangle":
                    append_list.append({
                        "type": obj.shape_name,
                        "coordinates": [obj.x1, obj.y1, obj.x2, obj.y2],
                        "color": obj.color,
                        "corner_style": obj.corner_style
                    })
            else:
                append_list.append({
                    "type": "group",
                    "objects": self.to_append_routine(drawn_obj.objects)
                })
        return append_list
    
    
    def save_drawing(self, filename):
        primitives_info = []
        groups_info = []
                
        for drawn_obj in self.canvas.drawn_objects:
            if drawn_obj.objects[0].is_primitive:
                actual_object = drawn_obj.objects[0]
                if actual_object.shape_name == "Line":
                    primitives_info.append({
                        "type": actual_object.shape_name,
                        "coordinates": [actual_object.x1, actual_object.y1, actual_object.x2, actual_object.y2],
                        "color": actual_object.color
                    })
                elif actual_object.shape_name == "Rectangle":
                    primitives_info.append({
                        "type": actual_object.shape_name,
                        "coordinates": [actual_object.x1, actual_object.y1, actual_object.x2, actual_object.y2],
                        "color": actual_object.color,
                        "corner_style": actual_object.corner_style
                    })
            else:
                group_info = {
                        "type": "group",
                        "objects": self.to_append_routine(drawn_obj.objects)
                    }
                
                groups_info.append(group_info)

        drawing_info = {"primitives": primitives_info, "groups": groups_info}

        with open(filename, "wb") as file:
            print(drawing_info)
            pickle.dump(drawing_info, file)
        print("Drawing saved successfully.")

    def import_drawing(self, filename):
        with open(filename, "rb") as file:
            drawing_info = pickle.load(file)
            print(drawing_info)
        if drawing_info:
            # Clear Canvas
            self.canvas.delete("all")

            for primitive_info in drawing_info["primitives"]:
                obj = self.create_object_from_info(primitive_info)
                if obj:
                    self.canvas.drawn_objects.append(obj)

            for group_info in drawing_info["groups"]:
                group_obj = DrawnObject(self.canvas)
                for obj_info in group_info["objects"]:
                    obj = self.create_object_from_info(obj_info)
                    if obj:
                        group_obj.add_object(obj)
                self.canvas.drawn_objects.append(group_obj)

            print("Drawing imported successfully.")
            
    def create_object_from_info(self, obj_info):
        shape_type = obj_info["type"]
        coordinates = obj_info["coordinates"]
        color = obj_info["color"]
        if shape_type == "Rectangle":
            obj = Rectangle(self.canvas)
            obj.corner_style = obj_info["corner_style"]
        elif shape_type == "Line":
            obj = Line(self.canvas)
        else:
            return None
        obj.x1, obj.y1, obj.x2, obj.y2 = coordinates
        obj.color = color
        
        obj.draw_shape()
        obj.drawn = True
        obj.on_release()
        drawobj = DrawnObject(self.canvas)
        drawobj.add_object(obj)
        return drawobj

def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
