from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

class Orvd():
    pass

def start_web():
    app.run(host='0.0.0.0', port=8000, threaded=True)