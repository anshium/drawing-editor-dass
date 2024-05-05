import pickle

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
