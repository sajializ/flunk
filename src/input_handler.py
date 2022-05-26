
class InputHandler:
    def __init__(self):
        pass

    def get_input(self):
        command = list(input("Enter command: ").split())

        if command[0] == "broadcast":
            return command[1]

        return None
    
    
