

import socket
import json
import finder


class Fluncaster:
    BROADCAST_ADDRESS = '<broadcast>'
    LISTEN_ADDRESS = ''
    CHUCK_SIZE = 4096
    PORT = 12345


    def __init__(self):
        self.finder = finder.Finder()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.connect((Fluncaster.BROADCAST_ADDRESS, Fluncaster.PORT))
        self.local_ip = s.getsockname()[0]
        s.close()
    
    def generate_message(self, properties, values):
        message = {}
        for property, value in zip(properties, values):
            message[property] = value
        return message

    def broadcast_request(self, filename):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        message = json.dumps(self.generate_message(['request'], [filename]))
        s.sendto(message.encode('utf-8'), (Fluncaster.BROADCAST_ADDRESS, Fluncaster.PORT))

        s.settimeout(1)
        result, address = s.recvfrom(Fluncaster.CHUCK_SIZE)
        result = json.loads((result.decode('utf-8')))['response'][0]
        print(result)
        path = result['name']
        size = result['size']

        response = json.dumps(self.generate_message(['download', 'port'], [path, 12346]))
        s.sendto(response.encode('utf-8'), address)

        self.receive(path)

        s.close()

    def listen(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address = (Fluncaster.LISTEN_ADDRESS, Fluncaster.PORT)
        s.bind(address)

        while True:
            data, address = s.recvfrom(Fluncaster.CHUCK_SIZE)
            
            if address[0] == self.local_ip:
                continue

            request = json.loads(data.decode('utf-8'))
            print(request)

            if 'request' in request.keys():
                result = self.finder.get_path(request['request'])
                if len(result):
                    response = json.dumps(self.generate_message(['response'], [result]))
                    s.sendto(response.encode('utf-8'), address)

            elif 'download' in request.keys():
                self.send(address[0], request['download'], request['port'])

    def send(self, address, path, port):
        tcp_socket = socket.socket()
        tcp_socket.connect((address, port))
        tcp_socket.send("SALAAAM")

    def receive(self, path):
        tcp_socket = socket.socket()
        tcp_socket.bind(("127.0.0.1", 12346))
        tcp_socket.listen(5)
        c, addr = tcp_socket.accept()
        l = c.recv(1024)
        print(l)