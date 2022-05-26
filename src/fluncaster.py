

import socket
import json


class Fluncaster:
    BROADCAST_ADDRESS = '<broadcast>'
    PORT = 12345


    def __init__(self):
        pass

    def generate_request(self, filename):
        return {
                "request": filename
            }

    def broadcast_request(self, filename):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        message = json.dumps(self.generate_request(filename))
        s.sendto(message.encode('utf-8'), (Fluncaster.BROADCAST_ADDRESS, Fluncaster.PORT))

        s.close()