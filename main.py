import tkinter as tk
import pickle
from tkinter import filedialog

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
    
    def export_to_xml(self, filename):
        with open(filename, "w") as file:
            file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file.write("<drawing>\n")
            self.export_objects_to_xml(self.canvas.drawn_objects, file)
            file.write("</drawing>\n")
        print("Drawing exported to XML successfully.")

    def export_objects_to_xml(self, drawn_objects, file, indent=0):
        indent_str = " " * indent
        for drawn_obj in drawn_objects:
            if drawn_obj.objects[0].is_primitive:
                actual_object = drawn_obj.objects[0]
                if actual_object.shape_name == "Line":
                    file.write(f"{indent_str}<line>\n")
                    file.write(f"{indent_str}  <begin>\n")
                    file.write(f"{indent_str}    <x>{actual_object.x1}</x>\n")
                    file.write(f"{indent_str}    <y>{actual_object.y1}</y>\n")
                    file.write(f"{indent_str}  </begin>\n")
                    file.write(f"{indent_str}  <end>\n")
                    file.write(f"{indent_str}    <x>{actual_object.x2}</x>\n")
                    file.write(f"{indent_str}    <y>{actual_object.y2}</y>\n")
                    file.write(f"{indent_str}  </end>\n")
                    file.write(f"{indent_str}  <color>{actual_object.color}</color>\n")
                    file.write(f"{indent_str}</line>\n")
                elif actual_object.shape_name == "Rectangle":
                    file.write(f"{indent_str}<rectangle>\n")
                    file.write(f"{indent_str}  <upper-left>\n")
                    file.write(f"{indent_str}    <x>{actual_object.x1}</x>\n")
                    file.write(f"{indent_str}    <y>{actual_object.y1}</y>\n")
                    file.write(f"{indent_str}  </upper-left>\n")
                    file.write(f"{indent_str}  <lower-right>\n")
                    file.write(f"{indent_str}    <x>{actual_object.x2}</x>\n")
                    file.write(f"{indent_str}    <y>{actual_object.y2}</y>\n")
                    file.write(f"{indent_str}  </lower-right>\n")
                    file.write(f"{indent_str}  <color>{actual_object.color}</color>\n")
                    file.write(f"{indent_str}  <corner>{actual_object.corner_style}</corner>\n")
                    file.write(f"{indent_str}</rectangle>\n")
            else:
                file.write(f"{indent_str}<group>\n")
                self.export_objects_to_xml(drawn_obj.objects, file, indent + 2)
                file.write(f"{indent_str}</group>\n")

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
