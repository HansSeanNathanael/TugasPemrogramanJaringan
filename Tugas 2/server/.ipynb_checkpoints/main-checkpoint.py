import server
import protocols
import protocol_interface
import logging

def main():
    logging.warning(f"Menjalankan server")
    main_server = server.Server("0.0.0.0", 45000, protocols.Protocols(protocol_interface.ProtocolInterface()))
    logging.warning(f"Server berhasil berjalan")
    main_server.start()

if __name__=="__main__":
    main()