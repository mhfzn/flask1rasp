from flask import Flask, jsonify, render_template
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

mqtt_server = "192.168.100.220"
mqtt_topic = "pnj_csc_TA_kel4"

total_spots = 0
available_spots = 0
spots_json = {}

# MQTT callback
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    global total_spots, available_spots, spots_json

    payload = msg.payload.decode()
    print(f"Message received: {payload}")

    spots_json = json.loads(payload)
    total_spots = len(spots_json)
    available_spots = sum([1 for spot in spots_json.values() if spot == 1])

# MQTT Setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_server, 1883, 60)

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')  # Assuming your HTML code is saved as 'templates/index.html'

@app.route('/spots')
def spots():
    return jsonify({
        'availableSpots': available_spots,
        'totalSpots': total_spots,
        'spots': spots_json
    })

def run_flask():
    app.run(host='0.0.0.0', port=5001)

if __name__ == '__main__':
    client.loop_start()  # Start the MQTT loop in a separate thread
    run_flask()  # Start the Flask web server
