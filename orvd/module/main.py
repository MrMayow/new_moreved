from flask import Flask, request, jsonify
import requests
import random 

app = Flask(__name__)

class Orvd():
    def __init__(self):
        pass

    @app.route('/route-check', methods=['POST'])
    def route_check():
        data = request.get_json()
        route = list(data.get("route"))
        result = False if (random.randint(0, 3) == 0) else True
        return jsonify({"route_approve": result}), 200


def start_web():
    app.run(host='0.0.0.0', port=8000, threaded=True)
    orvd = Orvd()