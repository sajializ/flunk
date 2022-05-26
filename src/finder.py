import os

class Finder:
    PATH = os.path.expanduser("~/Downloads")
    
    def __init__(self) -> None:
        pass

    def get_path(self, filename):
        result = []
        for root, dirs, files in os.walk(self.PATH):
            if filename in files:
                file_path = os.path.join(root, filename)
                file_size = os.path.getsize(file_path)
                result.append({"name": file_path, "size": file_size})
        return result

