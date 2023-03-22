import logging
import socket
import threading
import client_thread
import client_thread_list

class Server(threading.Thread):
    def __init__(self, ipaddress, port, protocols):
        self.address = (ipaddress, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.protocols = protocols
        
        threading.Thread.__init__(self)

    def run(self):
        self.server_socket.bind(self.address)
        self.server_socket.listen(1)
        
        client_thread_lists = client_thread_list.ClientThreadList()
        
        while True:
            connection, client_address = self.server_socket.accept()
            
            logging.warning(f"Koneksi baru terhubung {client_address}")
            
            client = client_thread.ClientThread(connection, client_address, self.protocols, client_thread_lists)
            client.start()
            
            