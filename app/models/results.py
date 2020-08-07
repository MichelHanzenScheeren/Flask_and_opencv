from datetime import datetime

class Results():
    def __init__(self):
        self.differentiator = []
        self.captures = []
        self.signals = []
        self.total_time = 0 
        self.captures_seg = 1
    

    def initialize_parameters(self, total_time, captures_seg):
        self.initial_date = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        self.captures = [] 
        self.signals = []
        self.total_time = total_time
        self.captures_seg = captures_seg
        self.interval = (1 / self.captures_seg)