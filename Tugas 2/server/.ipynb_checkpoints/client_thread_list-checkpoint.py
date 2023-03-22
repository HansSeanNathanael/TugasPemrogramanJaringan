# Kelas ClientThreadList digunakan untuk menyimpan ClientThread
# yang dibuat

class ClientThreadList:
    def __init__(self):
        self.list = set()
        
    def add_client_thread(self, client_thread):
        self.list.add(client_thread)
            
    def size(self):
        return len(self.list)
    
    def remove_client_thread(self, client_thread):
        self.list.remove(client_thread)
        
    