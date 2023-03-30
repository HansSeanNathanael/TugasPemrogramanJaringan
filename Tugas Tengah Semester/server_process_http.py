from socket import *
import socket
import multiprocessing
import time
import sys
import logging
from http import HttpServer

httpserver = HttpServer()

class ProcessTheClient(multiprocessing.Process):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        multiprocessing.Process.__init__(self)

    def run(self):
        print(self.connection)
        rcv=""
        while True:
            try:
                data = self.connection.recv(32)
                if data:
                    #merubah input dari socket (berupa bytes) ke dalam string
                    #agar bisa mendeteksi \r\n
                    d = data.decode()
                    rcv=rcv+d
                    if rcv[-4:]=='\r\n\r\n':
                        #end of command, proses string
                        logging.warning("data dari client: {}" . format(rcv))
                        hasil = httpserver.proses(rcv)
                        #hasil akan berupa bytes
                        #untuk bisa ditambahi dengan string, maka string harus di encode
                        hasil=hasil+"\r\n\r\n".encode()
                        logging.warning("balas ke  client: {}" . format(hasil))
                        #hasil sudah dalam bentuk bytes
                        self.connection.sendall(hasil)
                        rcv=""
                        try:
                            self.connection.shutdown(socket.SHUT_WR)
                        except:
                            pass
                        self.connection.close()
                        break
                else:
                    break
            except Exception as e:
                logging.warning(e)
        try:
            self.connection.shutdown(socket.SHUT_WR)
        except:
            pass
        self.connection.close()



class Server(multiprocessing.Process):
    def __init__(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        multiprocessing.Process.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 8889))
        self.my_socket.listen(1)
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning("connection from {}".format(self.client_address))

            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()



def main():
    svr = Server()
    svr.start()

if __name__=="__main__":
    main()

