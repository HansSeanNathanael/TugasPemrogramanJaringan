import socket
import logging
import thread_factory
import thread_pool_factory
import process_factory

def get_ip_addres(address):
    ip_address = address.split(":")
    
    return (ip_address[0], int(ip_address[1]))


if __name__ == "__main__":
    
    print("Masukkan ip server: ", end="")
    server_address = get_ip_addres(input())
    
    print("Pilih metode client: ")
    print("1. Thread")
    print("2. ThreadPool")
    print("3. Process")
    
    pilihan = int(input())
    
    if pilihan == 1:
        thread_factory.ThreadFactory(server_address)
    elif pilihan == 2:
        thread_pool_factory.ThreadpoolFactory(server_address)
    elif pilihan == 3:
        process_factory.ProcessFactory(server_address)