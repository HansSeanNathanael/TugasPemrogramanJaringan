import logging
import socket
import time
import concurrent.futures

TIME_REQUEST = "TIME\r\n".encode()

def thread_process(ip_address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(ip_address)
    
    for i in range(4):
        sock.sendall(TIME_REQUEST)
        response = sock.recv(32).decode()
        while response[-2:] != "\r\n":
            response = response + sock.recv(32).decode()
        print(f"{response[:-2]}")
        time.sleep(1)
    
    sock.close()
    
class ThreadpoolFactory:
    
    def __init__(self, ip_address):
        total_thread = 1
        tasks = []
        
        while True:
            task = concurrent.futures.ThreadPoolExecutor(max_workers=total_thread)
            for i in range(total_thread):
                tasks.append(task.submit(thread_process, ip_address))
                
            for i in range(total_thread):
                tasks[i].result()
                
            logging.warning(f"Total thread: {total_thread}")
            total_thread += 1