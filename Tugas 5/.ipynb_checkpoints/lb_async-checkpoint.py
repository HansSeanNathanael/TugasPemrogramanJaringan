import socket
import time
import sys
import asyncore
import logging

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
        self.current = 0
        
    def getserver(self):
        s = self.servers[self.current]
        
        self.current = self.current + 1
        if (self.current >= len(self.servers)):
            self.current = 0
        return s


class Backend(asyncore.dispatcher_with_send):
    def __init__(self, target_address):
        asyncore.dispatcher_with_send.__init__(self)
        
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(target_address)
        
    def set_handler(self, write_pipe, close_handler):
        self.write_pipe = write_pipe
        self.close_handler = close_handler
        
    def handle_read(self):
        try:
            self.write_pipe(self.recv(32))
        except:
            pass
        
        
    def handle_close(self):
        try:
            self.close_handler()
        except:
            pass


class ProcessTheClient(asyncore.dispatcher):
        
    def set_handler(self, write_pipe, close_handler):
        self.write_pipe = write_pipe
        self.close_handler = close_handler
        
    def handle_read(self):
        try:
            self.write_pipe(self.recv(32))
        except:
            pass
    
    def handle_close(self):
        try:
            self.close_handler()
        except:
            pass
        
class Bridge:
    def __init__(self, client_dispatcher, server_dispatcher):
        self.client_dispatcher = client_dispatcher
        self.server_dispatcher = server_dispatcher
        
        self.client_dispatcher.set_handler(self.send_to_server, self.close_connection)
        self.server_dispatcher.set_handler(self.send_to_client, self.close_connection)
        
    def close_connection(self):
        self.client_dispatcher.close()
        self.server_dispatcher.close()
        
    
    def send_to_client(self, message):
        self.client_dispatcher.send(message)
        
    def send_to_server(self, message):
        self.server_dispatcher.send(message)
        

class Server(asyncore.dispatcher):
    def __init__(self, portnumber, backend_list):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        
        self.bind(('0.0.0.0',portnumber))
        self.listen(5)
        self.backend_list = backend_list
        logging.warning("load balancer running on port {}" . format(portnumber))

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            socket, address = pair
            logging.warning("connection from {}" . format(repr(address)))

            backend_used_now = self.backend_list.getserver()
            logging.warning("koneksi dari {} diteruskan ke {}" . format(address, backend_used_now))
            
            bridge = Bridge(ProcessTheClient(socket), Backend(backend_used_now))
            
    
    def handle_close(self):
        self.close()

def main():
    portnumber=55555
    try:
        portnumber=int(sys.argv[1])
    except:
        pass
    
    ip_parser = IPParser()
    backend_list = BackendList(ip_parser.parse_addresses(sys.argv[2:]))
    
    svr = Server(portnumber, backend_list)
    asyncore.loop()

if __name__=="__main__":
    main()


