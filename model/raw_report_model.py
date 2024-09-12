class RawReportModel:
    id : int
    log_date : str
    scr_ip : str
    dst_port : str
    application : str
    total : int
    def __init__(self, id, log_date, scr_ip, dst_port, application, total):
        self.id = id
        self.log_date = log_date
        self.scr_ip = scr_ip
        self.dst_port = dst_port
        self.application = application
        self.total = total
        
        