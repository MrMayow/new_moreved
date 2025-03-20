from flask import Flask, request, jsonify
import time
import threading

app = Flask(__name__)


class Point:
    def __init__(self, uid, x, y):
        self.x = x
        self.y = y
        self.uid = uid

    def __repr__(self):
        return f"Point(uid={self.uid}, x={self.x}, y={self.y})"


class Boat:
    def __init__(self, coordinates_array):
        self.current_point = Point(0, 0, 0)
        self.is_moving = False
        self.route = self.format_route(coordinates_array)
        

    def format_route(self, coordinates_array):
        final_route = [self.current_point]
        for i, v in enumerate(coordinates_array):
            final_route.append(Point(i + 1, v[0], v[1]))
        return final_route

    def start_moving(self):
        self.is_moving = True
        while self.is_moving and self.current_point.uid < len(self.route) - 1:
            current_point = self.current_point
            next_point = self.route[self.current_point.uid + 1]
            print(f"Moving from {current_point} to {next_point}")
            self.move_to_point(current_point, next_point)
            self.current_point = next_point
            time.sleep(3)
        print("Route completed!")

    def move_to_point(self, current_point, next_point):
        print(f"Calculating direction from ({current_point.x}, {current_point.y}) to ({next_point.x}, {next_point.y})")
        print(f"Arrived at ({next_point.x}, {next_point.y})")


@app.route('/start_boat', methods=['POST'])
def start():
    data = request.get_json()
    route = list(data.get("route"))
    boat = Boat(route)
    threading.Thread(target=boat.start_moving).start()
    return jsonify({"status": "Boat started moving", "Point_count": len(boat.route)}), 200


def start_web():
    app.run(host='0.0.0.0', port=8000, threaded=True)