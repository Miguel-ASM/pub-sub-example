from flask_socketio import SocketIO
from redis import Redis
import json
from os import environ

redis_host = environ.get('REDIS_HOST')

redis_client = Redis(
    host=redis_host,
    port=6379,
    decode_responses=True
)

SUBSCRIPTIONS_MANAGING_CHANNEL = 'subscriptions'

pubsub = redis_client.pubsub()
pubsub.subscribe(SUBSCRIPTIONS_MANAGING_CHANNEL)
socketio = SocketIO(message_queue=f'redis://{redis_host}')


def main():
    for message in pubsub.listen():
        try:
          channel_received, message_type = message.get('channel'), message.get('type')
          if message_type != 'message': continue
          json_message = json.loads(message.get('data'))
          if channel_received == SUBSCRIPTIONS_MANAGING_CHANNEL:
              print(message.get('data'))
              action, channel = json_message.get('action'), json_message.get('channel')
              if action == 'subscribe': pubsub.subscribe(channel)
              if action == 'unsubscribe': pubsub.unsubscribe(channel)
          if channel_received != SUBSCRIPTIONS_MANAGING_CHANNEL:
              print(message.get('data'))
              socketio.emit('message',json_message )
        except Exception as e:
            print(e)
    

if __name__ == '__main__':
    main()
