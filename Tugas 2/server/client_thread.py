import socket
import threading
import logging

class ClientThread(threading.Thread):
    
    def __init__(self, connection, address, protocols):
        self.connection = connection
        self.address = address
        self.protocols = protocols
        
        threading.Thread.__init__(self)
        
    def run(self):
        
        while True:
            request = self.connection.recv(32)
            
            if request:
                request = request.decode()
                while request[-2:] != "\r\n":
                    request += self.connection.recv(32).decode()
                
                request = request[:-2]
                logging.warning(f"{self.address} request {request}")
                response = self.protocols.proses_request(request) + "\r\n"
                self.connection.sendall(response.encode())
                
            else:
                break
                
        self.connection.close()
        logging.warning(f"{self.address} putus koneksi")
            