import datetime, json
from backend_shared.logger import logger
from backend_shared.utils import date
class DBUtils:
    def __init__(self):
        self.logger = logger.Logger()
        self.dateUtils = date.DateUtils()

    def account_to_json(self, user):
        user_json = {}
        try:
            user_json = {
                "id": user[0],
                "mid": user[1],
                "username": user[2],
                "nickname": user[3],
                "email": user[6],
                "role":user[7],
                "sub_role":user[8]
            }
            return user_json
        except:
            return user_json   

    def split(self, item, type=None):
        try:
            if not item: return []
            if type == "number":
                res = []
                if "," in item: 
                    for i in item.split(","):
                        res.append(int(i.strip()))
                    return res
                return [int(item)]
            if "," in item: return item.split(",")
            return [item]
        except: return []


    def subscription_to_json(self, entry):
        video_json = {}
        try:
            video_json = {
                "user_id": entry[1],
                "item_id": entry[2],
                "isActive": self.dateUtils.isFuture(f"{entry[9]}")
            }
            return video_json
        except Exception as e:
            self.logger.log("ERROR", f"Can't create subscription-json: {e}")
            return video_json  
        
    def get_date_string(self):
        return datetime.datetime.now().strftime('%Y-%m-%d')
    
    def get_one_month_ago(self):
        return (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    
    def ist_older_than_18(self, geburtsdatum):
        values = str(geburtsdatum).split("-")
        today = datetime.datetime.now()
        eighteenyears = datetime.timedelta(days=18*365+5)
        date_of_birth = datetime.datetime(int(values[0]), int(values[1]), int(values[2]))
        return today - eighteenyears > date_of_birth