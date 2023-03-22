import socket
import logging

def get_ip_addres(address):
    ip_address = address.split(":")
    
    return (ip_address[0], int(ip_address[1]))


if __name__ == "__main__":
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(10.0)
    logging.warning("membuka socket")
    
    print("Masukkan ip server: ", end="")
    try:
        server_address = get_ip_addres(input())
        logging.warning(f"opening socket {server_address}")
        client_socket.connect(server_address)
        
        request = ""
        while True:
            request = input()
            
            if request.upper().strip() == "EXIT":
                break
            else:
                request += "\r\n"
                client_socket.sendall(request.encode('utf-8'))
                response = client_socket.recv(32)
                
                if response:
                    response = response.decode('utf-8')
                    while response[-2:] != "\r\n":
                        response = response + client_socket.recv(32).decode('utf-8')
                    print(f"{response[:-2]}")
                else:
                    logging.warning(f"Server terputus")
                    break
                
            request = ""
    
    except Exception as e:
        logging.warning(f"Gagal: {e}")
    finally:
        logging.warning(f"Koneksi dimatikan")
        client_socket.close()