class Protocols:
    def __init__(self, protocol_interface):
        self.interface = protocol_interface
        
    def proses_request(self, request):
        request_data = request.split(" ")
        request_command = request_data[0]
        params = request_data[1:]
        
        try:
            response = getattr(self.interface,request_command)(params)
            return response
        except Exception as e:
            return ""
        