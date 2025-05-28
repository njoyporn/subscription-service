from backend_shared.database import db_connection, db_utils, db_executer
from backend_shared.security import verifier, token, crypt
from backend_shared.logger import logger
from backend_shared.utils import rng, date
from backend_shared.types import BusinessResponse

class RequestHandler:
    def __init__(self, config):
        self.config = config
        self.db_connection = db_connection.Connection(self.config["database"]["hostname"], self.config["database"]["user"]["username"], self.config["database"]["user"]["password"], self.config["database"]["name"], self.config["database"]["port"])
        self.verifier = verifier.Verifier(self.db_connection, self.config)
        self.db_executer = db_executer.Executer(self.db_connection, self.config)
        self.db_utils = db_utils.DBUtils()
        self.logger = logger.Logger()
        self.random = rng.RNG()
        self.date = date.DateUtils()
        self.tokenizer = token.Tokenizer(self.config)
        self.crypt = crypt.Encrpyter(self.config)

    def get_subscription(self, request):
        try:
            id = request.args.get("id")
            user_id = request.args.get("user_id")
            subscription = self.db_executer.get_subscription(id, user_id)
            print(subscription)
            subscription_json = self.db_utils.subscription_to_json(subscription[0])
            return BusinessResponse(self.random.CreateRandomId(), "subscription", subscription_json).toJson()
        except Exception as e: 
            self.logger.log("ERROR", f"Can't handle get subscription || error => {e}")
            return BusinessResponse(self.random.CreateRandomId(), "error-get-subscription", []).toJson()

    def get_subscriptions(self, request):
        try:
            user_id = request.args.get("user_id")
            subscriptions = self.db_executer.get_subscriptions(user_id)
            result = []
            for subscription in subscriptions:
                result.append(self.db_utils.subscription_to_json(subscription))
            return BusinessResponse(self.random.CreateRandomId(), "subscriptions", result).toJson()
        except Exception as e: 
            self.logger.log("ERROR", f"Can't handle get subscription || error => {e}")
            return BusinessResponse(self.random.CreateRandomId(), "error-get-subscriptions", []).toJson()
        
    def create_subscription(self, request):
        try:
            data = request.json
            id = self.random.CreateRandomId()
            user_id = self.verifier.escape_characters(data['user_id'])
            item_id = self.verifier.escape_characters(data['item_id'])
            payed_amount = float(self.verifier.escape_characters(data['payed_amount']))
            payed_currency = self.verifier.escape_characters(data['payed_currency'])
            resource_type = self.verifier.escape_characters(data['resource_type'])
            event_type = self.verifier.escape_characters(data['event_type'])
            active_till = self.date.toDate(self.verifier.escape_characters(data['active_till']))
            self.db_executer.create_subscription(id, user_id, item_id, payed_amount, payed_currency, resource_type, event_type, active_till)
            return BusinessResponse(self.random.CreateRandomId(), "subscription created", {"id": id}).toJson()
        except Exception as e:
            self.logger.log("ERROR", f"Error creating subscription, {e}")
            return BusinessResponse(self.random.CreateRandomId(), "error-creating-subscription", []).toJson()
    