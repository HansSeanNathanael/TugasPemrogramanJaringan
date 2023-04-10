from socket import *
import socket
import threading
import logging
import time
import sys


from file_protocol import  FileProtocol
fp = FileProtocol()


class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        data_received = ""
        while True:
            data = self.connection.recv(32)
            if data:
                data_received += data.decode()
                
                if data_received[-4:] == "\r\n\r\n":
                    hasil = fp.proses_string(data_received)
                    hasil=hasil+"\r\n\r\n"
                    self.connection.sendall(hasil.encode())
                    
                    data_received = ""
            else:
                break
        self.connection.close()


class Server(threading.Thread):
    def __init__(self, server_ipaddress, server_port):
        self.ipinfo = (server_ipaddress, server_port)
        self.the_clients = set()
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        threading.Thread.__init__(self)

    def run(self):
        logging.warning(f"server berjalan di ip address {self.ipinfo}")
        self.server_socket.bind(self.ipinfo)
        self.server_socket.listen(1)
        
        while True:
            self.connection, self.client_address = self.server_socket.accept()
            logging.warning(f"connection from {self.client_address}")

            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            
            self.the_clients.add(clt)


def main():
    server_ipaddress = "0.0.0.0"
    server_port = 6666
    try:
        server_port = int(sys.argv[1])
    except:
        pass
    
    svr = Server(server_ipaddress, server_port)
    svr.start()


if __name__ == "__main__":
    main()

