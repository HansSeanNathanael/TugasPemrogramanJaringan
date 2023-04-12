import socket
import time
import sys
import logging
import multiprocessing
import concurrent.futures

class IPParser:
    def parse_address(self, address):
        splitted_address = address.split(":")
        return (splitted_address[0], int(splitted_address[1]))
    
    def parse_addresses(self, addresses):
        address_list = []
        for address in addresses:
            address_list.append(self.parse_address(address))
            
        return address_list
    
    
class BackendList:
    def __init__(self, servers = []):
        self.servers = servers
        self.current=0
        
    def getserver(self):
        s = self.servers[self.current]
        
        self.current = self.current + 1
        if (self.current >= len(self.servers)):
            self.current = 0
        return s




def ProcessTheClient(client_socket, backend_socket):
    try:
        while True:
            datafrom_client = client_socket.recv(1024)
            if datafrom_client:
                backend_socket.sendall(datafrom_client)
            else:
                client_socket.shutdown(socket.SHUT_RDWR)
                backend_socket.shutdown(socket.SHUT_RDWR)

            datafrom_backend = backend_socket.recv(1024)
            if datafrom_backend:
                client_socket.sendall(datafrom_backend)
            else:
                client_socket.shutdown(socket.SHUT_RDWR)
                backend_socket.shutdown(socket.SHUT_RDWR)
    except:
        pass
    
    try:
        backend_socket.close()
    except:
        pass
    
    try:
        client_socket.close()
    except:
        pass
    
    return



def Server():
    server_address = ("0.0.0.0", int(sys.argv[1]))
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen(1)
    
    ip_parser = IPParser()
    backend = BackendList(ip_parser.parse_addresses(sys.argv[2:]))

    with concurrent.futures.ProcessPoolExecutor(20) as executor:
        while True:
            connection, client_address = server_socket.accept()
            
            backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            backend_used_now = backend.getserver()
            
            logging.warning(f"{client_address} connecting to {backend_used_now}")
            backend_socket.connect(backend_used_now)

            client_process = executor.submit(ProcessTheClient, connection, backend_socket)


def main():
    Server()

if __name__=="__main__":
    main()

