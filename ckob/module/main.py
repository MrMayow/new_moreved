from flask import Flask, request, jsonify
import requests
import random

app = Flask(__name__)

BOAT_START_URL = "http://boat:8000/start_boat"
ORVD_ROUTE_CHECK_URL = "http://orvd:8000/route-check"

class Ckob:
    def __init__(self):
        self.route = []


    def send_route_to_boat(self, route):
        try:
            payload = {"route": route}
            response = requests.post(BOAT_START_URL, json=payload)
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
        

    def generate_random_route(self, num_points=5, x_range=(0, 100), y_range=(0, 100)):
        route = []
        for _ in range(num_points):
            x = random.randint(x_range[0], x_range[1])
            y = random.randint(y_range[0], y_range[1])
            route.append([x, y])
        return route
    

    def request_route_approve(self, route):
        try:
            print(f"Request root approve from ORVD")
            payload = {"route": route}
            response = requests.post(ORVD_ROUTE_CHECK_URL, json=payload)
            json_data = response.json()
            return json_data.get("route_approve")
        except Exception as e:
            return {"status": "error", "message": str(e)}


    def send_random_route(self):
        root_approve = False
        while not root_approve:
            random_route = self.generate_random_route()
            root_approve = self.request_route_approve(random_route)
            if root_approve:
                self.route = random_route

        result = self.send_route_to_boat(self.route)
        return jsonify(result), 200


@app.route('/start', methods=['GET'])
def start():
    root_approve = False
    while not root_approve:
        ckob = Ckob()
        ckob.send_random_route()


def start_web():
    app.run(host='0.0.0.0', port=8000, threaded=True)
    