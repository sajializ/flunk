import os

class Finder:
    PATH = os.path.expanduser("~/Downloads")
    
    def __init__(self) -> None:
        pass

    def get_path(self, filename):
        result = []
        for root, dirs, files in os.walk(self.PATH):
            if filename in files:
                result.append(os.path.join(root, filename))
        return result

