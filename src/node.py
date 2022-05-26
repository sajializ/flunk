import fluncaster

class Node:

    def __init__(self):
        self.fluncaster = fluncaster.Fluncaster()



n = Node()
n.fluncaster.broadcast_request("salam.txt")