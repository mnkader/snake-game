import arrow

class GenericLogger:
    def __init__(self, log_file_name, path):
        self.path = path
        self.todays_date = arrow.now('UTC+2').format(fmt='YYYY-MM-DD')
        self.name: str = log_file_name + '_' + self.todays_date
        self.log_file = open(path + self.name, 'a')
    
    def log(self, data_to_write):
        if self.todays_date != arrow.now('UTC+2').format(fmt='YYYY-MM-DD'):
            self.todays_date = arrow.now('UTC+2').format(fmt='YYYY-MM-DD')
        self.log_file = open(self.path + self.name, 'a')
        self.log_file.write(arrow.now('UTC+2').format(fmt='YYYY-MM-DD HH:mm:ss.SSS') + ' :: ' + data_to_write)
        self.log_file.write('\n')
        self.log_file.close()