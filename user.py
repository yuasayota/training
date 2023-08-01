class User:
    def __init__(self):
        self.training_setting()
    
    def training_setting(self,training_name, num_set, rep, num_time):
        self.TRAINING = training_name
        self.Number_SET = num_set
        self.Number_REP = rep
        self.REST_TIME = num_time
