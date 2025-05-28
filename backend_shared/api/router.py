from flask import Flask, request
from .requestHandler import RequestHandler
import os
api = Flask(__name__)

request_handler = None
base_route = "/api/v1"
data_path = f"{os.getcwd()}/binarys"

@api.route("/", methods=["GET"])
def index():
    return "200 OK from subscription-service"

@api.route(f"{base_route}/healthz", methods=["GET"])
def healthz():
    return "200 OK from subscription-service"

@api.route(f"{base_route}/subscription", methods=["GET"])
def get_subscription():
    return request_handler.get_subscription(request)

@api.route(f"{base_route}/subscriptions", methods=["GET"])
def get_subscriptions():
    return request_handler.get_subscriptions(request)

@api.route(f"{base_route}/subscription", methods=["POST"])
def create_subscription():
    return request_handler.create_subscription(request)

def run(conf):
    global config, request_handler
    config = conf
    request_handler = RequestHandler(config)
    if config["subscription_service"]["cors_enabled"]:
        from flask_cors import CORS
        cors = CORS(api)
    api.run(host=config["subscription_service"]["hostname"], port=config["subscription_service"]["port"])
