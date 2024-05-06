import pickle
from shapes_and_drawn_object import *

class FileHandler:
    def __init__(self, app) -> None:
        self.app = app
    
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
        
    def export_to_xml():
        pass

        
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
                
        for drawn_obj in self.app.canvas.drawn_objects:
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
            self.app.canvas.delete("all")

            for primitive_info in drawing_info["primitives"]:
                obj = self.create_object_from_info(primitive_info)
                if obj:
                    self.app.canvas.drawn_objects.append(obj)

            for group_info in drawing_info["groups"]:
                group_obj = DrawnObject(self.app.canvas)
                for obj_info in group_info["objects"]:
                    obj = self.create_object_from_info(obj_info)
                    if obj:
                        group_obj.add_object(obj)
                self.app.canvas.drawn_objects.append(group_obj)

            print("Drawing imported successfully.")
            
    def create_object_from_info(self, obj_info):
        shape_type = obj_info["type"]
        coordinates = obj_info["coordinates"]
        color = obj_info["color"]
        if shape_type == "Rectangle":
            obj = Rectangle(self.app.canvas)
            obj.corner_style = obj_info["corner_style"]
        elif shape_type == "Line":
            obj = Line(self.app.canvas)
        else:
            return None
        obj.x1, obj.y1, obj.x2, obj.y2 = coordinates
        obj.color = color
        
        obj.draw_shape()
        obj.drawn = True
        obj.on_release()
        drawobj = DrawnObject(self.app.canvas)
        drawobj.add_object(obj)
        return drawobj
    
    def export_to_xml(self, filename):
        with open(filename, "w") as file:
            file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
            file.write("<drawing>\n")
            self.export_objects_to_xml(self.app.canvas.drawn_objects, file)
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
                
    def export_to_ascii(self, filename):
        with open(filename, "w") as file:
            for drawn_obj in self.app.canvas.drawn_objects:
                self.export_object_to_ascii(drawn_obj, file)
        print("Drawing exported to ASCII successfully.")

    def export_object_to_ascii(self, drawn_obj, file, depth=0):
        indent = "  " * depth
        if drawn_obj.objects[0].is_primitive:
            actual_object = drawn_obj.objects[0]
            if actual_object.shape_name == "Line":
                file.write(f"{indent}line {actual_object.x1} {actual_object.y1} {actual_object.x2} {actual_object.y2} {actual_object.color}\n")
            elif actual_object.shape_name == "Rectangle":
                file.write(f"{indent}rect {actual_object.x1} {actual_object.y1} {actual_object.x2} {actual_object.y2} {actual_object.color} {actual_object.corner_style}\n")
        else:
            file.write(f"{indent}begin\n")
            for obj in drawn_obj.objects:
                self.export_object_to_ascii(obj, file, depth + 1)
            file.write(f"{indent}end\n")

    def import_from_ascii(self, filename):
        with open(filename, "r") as file:
            lines = file.readlines()
            self.app.canvas.delete("all")  # Clear Canvas
            self.import_objects_from_ascii(lines, self.app.canvas)
        print("Drawing imported from ASCII successfully.")

    def import_objects_from_ascii(self, lines, to_add_to, index=0, depth=0):
        while index < len(lines):
            line = lines[index].strip()
            if line.startswith("line"):
                _, x1, y1, x2, y2, color = line.split()
                line_obj = Line(self.app.canvas)
                line_obj.x1, line_obj.y1 = int(x1), int(y1)
                line_obj.x2, line_obj.y2 = int(x2), int(y2)
                line_obj.color = color
                line_obj.draw_shape()
                line_obj.drawn = True
                line_obj.on_release()
                drawn_obj = DrawnObject(self.app.canvas)
                drawn_obj.add_object(line_obj)
                if(depth == 0):
                    to_add_to.drawn_objects.append(drawn_obj)
                else:
                    to_add_to.add_object(drawn_obj)
                index += 1
            elif line.startswith("rect"):
                _, x1, y1, x2, y2, color, corner_style = line.split()
                rect_obj = Rectangle(self.app.canvas)
                rect_obj.x1, rect_obj.y1 = int(x1), int(y1)
                rect_obj.x2, rect_obj.y2 = int(x2), int(y2)
                rect_obj.color = color
                rect_obj.corner_style = corner_style
                rect_obj.draw_shape()
                rect_obj.drawn = True
                rect_obj.on_release()
                drawn_obj = DrawnObject(self.app.canvas)
                drawn_obj.add_object(rect_obj)
                if(depth == 0):
                    to_add_to.drawn_objects.append(drawn_obj)
                else:
                    to_add_to.add_object(drawn_obj)
                index += 1
            elif line.startswith("begin"):
                group_obj = DrawnObject(self.app.canvas)
                index += 1
                index = self.import_objects_from_ascii(lines, group_obj, index, depth + 1)
                if(depth == 0):
                    to_add_to.drawn_objects.append(group_obj)
                else:
                    to_add_to.add_object(group_obj)
                
            elif line.startswith("end"):
                return index + 1
            else:
                index += 1
        return index