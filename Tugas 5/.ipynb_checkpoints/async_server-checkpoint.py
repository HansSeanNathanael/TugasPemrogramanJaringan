import socket
import time
import sys
import asyncore
import logging
import http

httpserver = http.HttpServer()

received = ""

class ProcessTheClient(asyncore.dispatcher_with_send):
    def handle_read(self):
        global received
        while True:
            try:
                data = self.recv(32)
                if data:
                    received = received + data.decode()

                    if received[-4:]=='\r\n\r\n':
                        logging.warning("data dari client: {}" . format(received))
                        hasil = httpserver.proses(received)

                        hasil = hasil + "\r\n\r\n".encode()
                        logging.warning("balas ke  client: {}" . format(hasil))

                        self.send(hasil)
                        received = ""
                        self.close()
                        break
                else:
                    break
            except OSError as e:
                break
            except Exception as e:
                print(e)

        try:
            self.shutdown(socket.SHUT_WR)
            self.close()
        except:
            pass

class Server(asyncore.dispatcher):
    def __init__(self, portnumber):
        asyncore.dispatcher.__init__(self)
        
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        
        self.bind(("0.0.0.0",portnumber))
        self.listen(10)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            client_socket, client_address = pair
            logging.warning("connection from {}" . format(repr(client_address)))
            handler = ProcessTheClient(client_socket)

def main():
    portnumber=8000
    try:
        portnumber=int(sys.argv[1])
    except:
        pass
    svr = Server(portnumber)
    asyncore.loop()

if __name__=="__main__":
    main()

