import sys
import socket
import json
import base64
import logging
import shlex

server_address=('0.0.0.0',7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    
    if command_str[-4:] != "\r\n\r\n":
        command_str += "\r\n\r\n"
    
    try:
        logging.warning(f"sending message")
        sock.sendall(command_str.encode())
        data_received=""
        
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if data_received[-4:] == "\r\n\r\n":
                    break
            else:
                break
        hasil = json.loads(data_received)
        logging.warning(f"data received from server: {hasil}")
        return hasil
    except:
        logging.warning("error during data receiving")
        return False
    sock.close()


def remote_list(params=[]):
    command_str=f"LIST"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal request daftar file")
        return False

def remote_get(params=[]):
    command_str=f"GET {params[0]}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        print("Berhasil")
        return True
    else:
        print("Gagal")
        return False

def remote_put(params=[]):
    try: 
        fp = open(params[1], "rb")
        file_bytes = fp.read()
        command_str=f"PUT {params[0]} {base64.b64encode(file_bytes).decode()}"
        fp.close()
        
        # print(command_str)
        hasil = send_command(command_str)
        if (hasil['status']=='OK'):
            print("Berhasil")
            return True
        else:
            print("Gagal")
            return False
    except Exception as e:
        print(str(e))
        return false
    
def remote_delete(params=[]):
    command_str=f"DELETE {params[0]}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("Berhasil")
        return True
    else:
        print("Gagal")
        return False

def get_address(ip_adddress_with_port):
    ip_address_split = ip_adddress_with_port.split(":")
    return (ip_address_split[0], int(ip_address_split[1]))

    
if __name__=='__main__':
    
    try:
        server_address= get_address(sys.argv[1])
        
        commands = {"get": remote_get, "list": remote_list, "put": remote_put, "delete": remote_delete}
    
        while True:
            print("Masukkan command:")
            print("GET NAMAFILE - untuk mengunduh file dari server")
            print("LIST - untuk mengambil daftar nama file pada server")
            print("PUT NAMASIMPAN NAMALOKAL - untuk menyimpan file dengan nama NAMALOKAL pada server dengan nama NAMASIMPAN")
            print("DELETE NAMAFILE - untuk menghapus file NAMAFILE pada server")
            command = input()

            c = shlex.split(command.lower())
            c_request = c[0].strip()
            params = [x for x in c[1:]]

            try:
                commands[c_request](params)
            except Exception as e:
                print(str(e))
        
    except Exception as e:
        print(str(e))
