import datetime

class DateUtils:
    def __init__(self):
        pass

    def isFuture(self, dateString, pattern="%Y-%m-%d %H:%M:%S"):
        return datetime.datetime.strptime(dateString, pattern) > datetime.datetime.now()

    def toDate(self, dateString, pattern="%Y-%m-%d %H:%M:%S"):
        return datetime.datetime.strptime(dateString, pattern)