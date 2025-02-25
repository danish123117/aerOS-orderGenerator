from flask import Flask, render_template, jsonify, Response
from flask import request as frequest
import subprocess
import os
import signal
import time
import threading
from ngsiOperations.ngsildOperations.ngsildEntityCreator import ngsi_subscribe_DOG, ngsi_setup_DOG
from waitress import serve


app = Flask(__name__)
order_process = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_order():
    global order_process
    if order_process is None:
        freq = frequest.json.get("frequency")
        order_process = subprocess.Popen(["python", "order.py", freq])
        return jsonify({"status": "started"}), 200
    return jsonify({"status": "already running"}), 400

@app.route('/stop', methods=['POST'])
def stop_order():
    global order_process
    if order_process:
        os.kill(order_process.pid, signal.SIGTERM)
        order_process = None
        return jsonify({"status": "stopped"}), 200
    return jsonify({"status": "not running"}), 400

def generate_orders():
    """ Read order updates dynamically """
    while True:
        try:
            with open("orders.log", "r") as f:
                lines = f.readlines()
                for line in lines:
                    yield f"data: {line.strip()}\n\n"
                time.sleep(1)
        except FileNotFoundError:
            pass

@app.route('/stream')
def stream():
    return Response(generate_orders(), mimetype='text/event-stream')

@app.route('/setup')
def setup():
    orion = os.getenv("ORION_LD_HOST", 'localhost')
    orion_port = int(os.getenv("ORION_LD_PORT", 1026))
    context = os.getenv("CONTEXT_HOST", 'localhost')
    context_port = int(os.getenv("CONTEXT_PORT", 5051))
    notify_host = os.getenv("NOTIFY_HOST", 'localhost')
    notify_port = os.getenv("NOTIFY_PORT", 3030)
    notify_endpoint = f"http://{notify_host}:{notify_port}/notify"
    dog_status = ngsi_setup_DOG(orion,orion_port,context,context_port)
    subscribe_status = ngsi_subscribe_DOG(orion,orion_port,context,context_port,notify_endpoint)
       
    return dog_status.text, subscribe_status.text 

if __name__ == '__main__':
    print("Starting server on http://0.0.0.0:3020")
    serve(app, host='0.0.0.0', port=3020)


