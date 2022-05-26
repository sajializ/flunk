

import socket
import json


class Fluncaster:
    BROADCAST_ADDRESS = '<broadcast>'
    LISTEN_ADDRESS = ''
    CHUCK_SIZE = 4096
    PORT = 12345


    def __init__(self):
        self.local_ip = socket.gethostname()

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

    def listen(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = (Fluncaster.LISTEN_ADDRESS, Fluncaster.PORT)
        s.bind(address)

        while True:
            data, address = s.recvfrom(Fluncaster.CHUCK_SIZE)
            if address[0] == self.local_ip:
                continue

            request = json.loads(data.decode('utf-8'))['request']
            print(f"Received: {request} \n")
