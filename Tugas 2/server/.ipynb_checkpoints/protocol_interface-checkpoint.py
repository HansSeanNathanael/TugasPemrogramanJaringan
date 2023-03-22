import datetime

class ProtocolInterface:
    def __init__(self):
        pass

    def TIME(self, params=[]):
        if len(params) > 0:
            raise Exception()
        
        current_time = datetime.datetime.now()
        
        return f"JAM {current_time.hour}:{current_time.minute}:{current_time.second}"
        