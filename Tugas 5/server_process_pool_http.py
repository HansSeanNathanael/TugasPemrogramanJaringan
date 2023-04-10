import socket
import time
import sys
import logging
import multiprocessing
import concurrent.futures
import http

httpserver = http.HttpServer()

def ProcessTheClient(connection,address):
    received = ""
    while True:
        try:
            data = connection.recv(32)
            if data:
                received = received + data.decode()
                
                if received[-4:]=='\r\n\r\n':
                    logging.warning("data dari client: {}" . format(received))
                    hasil = httpserver.proses(received)
                    
                    hasil = hasil + "\r\n\r\n".encode()
                    logging.warning("balas ke  client: {}" . format(hasil))
                    
                    connection.sendall(hasil)
                    received = ""
                    connection.close()
                    return
            else:
                break
        except OSError as e:
            break
        except Exception as e:
            print(e)
    
    try:
        connection.shutdown(socket.SHUT_WR)
        connection.close()
    except:
        pass
    
    return



def Server(portnumber = 8889):
    the_clients = set()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(('0.0.0.0', portnumber))
    server_socket.listen(1)

    with concurrent.futures.ProcessPoolExecutor(20) as executor:
        while True:
            connection, client_address = server_socket.accept()
            client_process = executor.submit(ProcessTheClient, connection, client_address)
            the_clients.add(client_process)
            
            should_deleted = []
            for client_future in the_clients:
                if not client_future.running():
                    should_deleted.append(client_future)
            for client_future in should_deleted:
                the_clients.remove(client_future)
            
            print(f"Jumlah client yang terhubung {len(the_clients)}")





def main():
    portnumber=8000
    try:
        portnumber=int(sys.argv[1])
    except:
        pass
    svr = Server(portnumber)

if __name__=="__main__":
    main()

