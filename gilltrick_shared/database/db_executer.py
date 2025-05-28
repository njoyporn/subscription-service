import datetime, re
from backend_shared.logger import logger

class Executer:
    def __init__(self, connection, config):
        self.connection = connection
        self.config = config
        self.logger = logger.Logger()

    def create_subscription(self, id, user_id, item_id, payment_amount, payed_currency, resource_type, event_type, active_till):
        rc, result = self.connection.execute(f'''insert into {self.config["database"]["name"]}.{self.config["database"]["tables"][0]["name"]} (
                                id,
                                user_id,            
                                item_id, 
                                payed_amount, 
                                payed_currency, 
                                resource_type, 
                                event_type,
                                created_at,
                                updated_at,
                                active_till) 
                                values (
                                '{id}',
                                '{user_id}', 
                                '{item_id}', 
                                {payment_amount}, 
                                '{payed_currency}',
                                '{resource_type}',
                                '{event_type}',
                                '{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}',
                                '{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}',
                                '{datetime.datetime.strftime(active_till, '%Y-%m-%dT%H:%M:%S')}')''')
        return result
    
    def get_subscription(self, id, user_id):
        rc, result = self.connection.execute(f'''select * from {self.config["database"]["name"]}.{self.config["database"]["tables"][0]["name"]} where id = "{id}" and user_id = "{user_id}"''')
        return result

    def get_subscriptions(self, user_id):
        rc, result = self.connection.execute(f'''select * from {self.config["database"]["name"]}.{self.config["database"]["tables"][0]["name"]} where user_id = "{user_id}"''')
        return result