import multiprocessing
import socket
import time
import logging

TIME_REQUEST = "TIME\r\n".encode()

def process_main(ip_address, total_process):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(ip_address)
    total_process.value += 1
    logging.warning(f"Total process: {total_process.value}")
    
    while True:
        time.sleep(1)
        sock.sendall(TIME_REQUEST)
        response = sock.recv(32)
        
        if response:
            response = response.decode()
            while response[-2:] != "\r\n":
                response = response + sock.recv(32).decode()
            print(f"{response[:-2]}")
        else:
            logging.warning(f"Server terputus")
            break
            
    sock.close()
    total_process.value -= 1
    logging.warning(f"Total process: {total_process.value}")

class ProcessFactory:
    
    def __init__(self, ip_address):
        total_process = multiprocessing.Value("i", 0)
        
        while True:
            time.sleep(2)
            try:
                new_process = multiprocessing.Process(target=process_main, args=[ip_address, total_process])
                new_process.start()
            except Exception as e:
                logging.warning(f"Total process: {total_process.value}")