import threading
import socket
import time

TIME_REQUEST = "TIME\r\n".encode()

class ClientThread(threading.Thread):
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.ip_address)
        
        threading.Thread.__init__(self)
        
    def run(self):
        while True:
            time.sleep(1)
            self.socket.sendall(TIME_REQUEST)
            response = self.socket.recv(32)

            if response:
                response = response.decode()
                while response[-2:] != "\r\n":
                    response = response + self.socket.recv(32).decode()
                print(f"{response[:-2]}")
            else:
                logging.warning(f"Server terputus")
                break
                
        self.socket.close()
            