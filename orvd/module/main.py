from flask import Flask, request, jsonify
import requests
import random

app = Flask(__name__)

BOAT_START_URL = "http://boat:8000/start_boat"

class Orvd:
    def __init__(self):
        pass

    def send_route_to_boat(self, route):
        try:
            payload = {"route": route}
            response = requests.post(BOAT_START_URL, json=payload)
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}


def generate_random_route(num_points=5, x_range=(0, 100), y_range=(0, 100)):
    route = []
    for _ in range(num_points):
        x = random.randint(x_range[0], x_range[1])
        y = random.randint(y_range[0], y_range[1])
        route.append([x, y])
    return route


@app.route('/send_random_route', methods=['GET'])
def send_random_route():
    random_route = generate_random_route()
    print(f"Generated random route: {random_route}")
    orvd = Orvd()
    result = orvd.send_route_to_boat(random_route)
    return jsonify(result), 200


def start_web():
    app.run(host='0.0.0.0', port=8000, threaded=True)
