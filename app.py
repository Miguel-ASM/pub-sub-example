import json
from flask_socketio import SocketIO
from flask import Flask, render_template, request
from flask_cors import CORS
from redis import Redis
import eventlet
from os import environ


eventlet.monkey_patch()

print('------------')
print(environ.get('REDIS_HOST'))
print(environ.get('REDIS_HOST'))
print(environ.get('REDIS_HOST'))
print(environ.get('REDIS_HOST'))
print('------------')

redis_host = environ.get('REDIS_HOST')

redis_client = Redis(
    host=redis_host,
    port=6379,
    decode_responses=True
)


pubsub = redis_client.pubsub()

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your secret key
socketio = SocketIO(app, message_queue=f'redis://{redis_host}')


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/track')
def track():
    location_data = request.json
    print(location_data)
    redis_client.publish('real_life_location', json.dumps(location_data))
    return {'status': 'OK'}


@socketio.on('message')
def handle_message(data):
    message = data['message']
    print(f"Received message: {message}")
    socketio.emit('message', {'message': message})


@socketio.on('server_message')  # Add a new event for server messages
def handle_server_message(data):
    message = data['message']
    print(f"Server sent message: {message}")
    socketio.emit('message', {'message': message})


@socketio.on('connect')
def test_connect(auth):
    redis_client.publish('subscriptions', json.dumps(
        {'action': 'subscribe', 'channel': 'real_life_location'}))


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    redis_client.publish('subscriptions', json.dumps(
        {'action': 'unsubscribe', 'channel': 'real_life_location'}))
    print('Client disconnected')


def run_app():
    socketio.run(app, debug=True, host='0.0.0.0')


if __name__ == '__main__':
    run_app()
