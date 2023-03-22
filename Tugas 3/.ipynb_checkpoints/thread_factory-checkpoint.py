import client_thread
import time
import logging

class ThreadFactory:
    
    def __init__(self, ip_address):
        total_thread_dibuat = 0
        
        while True:
            time.sleep(2)
            try:
                client = client_thread.ClientThread(ip_address)
                client.start()
                total_thread_dibuat += 1
            finally:
                logging.warning(f"Total thread: {total_thread_dibuat}")