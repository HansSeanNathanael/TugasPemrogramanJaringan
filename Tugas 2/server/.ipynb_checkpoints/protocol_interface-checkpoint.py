import datetime

class ProtocolInterface:
    def __init__(self):
        pass

    def TIME(self, params=[]):
        if len(params) > 0:
            raise Exception()
        
        current_time = datetime.datetime.now()
        
        return f"JAM {current_time.hour:02d}:{current_time.minute:02d}:{current_time.second:02d}"
        