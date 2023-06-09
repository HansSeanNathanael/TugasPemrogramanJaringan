import socket
import threading
import logging

class ClientThread(threading.Thread):
    
    def __init__(self, connection, address, protocols, client_thread_list):
        self.connection = connection
        self.address = address
        self.protocols = protocols
        self.client_thread_list = client_thread_list
        self.client_thread_list.add_client_thread(self)
        logging.warning(f"Total koneksi terhubung {self.client_thread_list.size()}")
        
        threading.Thread.__init__(self)
        
    def run(self):
        
        while True:
            request = self.connection.recv(32)
            
            if request:
                request = request.decode('utf-8')
                while request[-2:] != "\r\n":
                    request += self.connection.recv(32).decode('utf-8')
                
                request = request[:-2]
                logging.warning(f"{self.address} request {request}")
                response = self.protocols.proses_request(request) + "\r\n"
                self.connection.sendall(response.encode('utf-8'))
                
            else:
                break
                
        self.connection.close()
        self.client_thread_list.remove_client_thread(self)
        logging.warning(f"{self.address} putus koneksi")
        logging.warning(f"Total koneksi terhubung {self.client_thread_list.size()}")
            