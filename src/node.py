import fluncaster
import input_handler
from multiprocessing import Process

class Node:

    def __init__(self):
        self.fluncaster = fluncaster.Fluncaster()
        self.input_handler = input_handler.InputHandler()


if __name__ == "__main__":
    node = Node()
    listen_process = Process(target=node.fluncaster.listen, args=())
    listen_process.start()

    while True:
        filename = node.input_handler.get_input()
        p = Process(target=node.fluncaster.broadcast_request, args=(filename,))
        p.start()
