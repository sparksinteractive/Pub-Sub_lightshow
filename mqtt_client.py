#!/usr/bin/python

import datetime
import time
import jwt
import json
import paho.mqtt.client as mqtt


ssl_private_key_filepath = '/home/pi/.ssh/demo_private.pem'
ssl_algorithm = 'RS256'
root_cert_filepath = '/home/pi/.ssh/roots.pem'
project_id = 'pubsub18'
gcp_location = 'us-central1'
registry_id = 'masterpi'
device_id = 'pi01'

_CLIENT_ID = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(project_id, gcp_location, registry_id, device_id)
_MQTT_TOPIC = '/devices/{}/events'.format(device_id)
_MQTT_CONFIG_TOPIC = '/devices/{}/config'.format(device_id)

_CLIENT_CONN_HOSTNAME = 'mqtt.googleapis.com'
_CLIENT_CONN_PORT = 8883

def create_jwt():
    cur_time = datetime.datetime.utcnow()
    token = {
        'iat': cur_time,
        'exp': cur_time + datetime.timedelta(minutes=60),
        'aud': project_id
    }
    with open(ssl_private_key_filepath, 'r') as f:
      private_key = f.read()
    return jwt.encode(token, private_key, algorithm=ssl_algorithm) # Assuming RSA, but also supports ECC

def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return '{}: {}'.format(rc, mqtt.error_string(rc))

class Object(object):
    pass

class ClientCallback(object):
    def __init__(self, on_handle_message):
        self.connected = False
        self.on_handle_message = on_handle_message

    def wait_for_connection(self, timeout):
        total_time = 0
        while not self.connected and total_time < timeout:
            time.sleep(1)
            total_time += 1

        if not self.connected:
            raise RuntimeError('Could not connect to MQTT bridge (timed out)')

    def on_connect(self, unused_client, unused_userdata, unused_flags, rc):
        print('Connection Result:', error_str(rc))
        self.connected = True

    def on_disconnect(self, unused_client, unused_userdata, rc):
        print('Disconnected:', error_str(rc))
        self.connected = False

    def on_publish(self, unused_client, unused_userdata, unused_mid):
        # print('Published message acked.')
        return

    def on_subscribe(self, unused_client, unused_userdata, unused_mid,
                     granted_qos):
        print('Subscribed: ', granted_qos)
        if granted_qos[0] == 128:
            print('Subscription failed.')

    def on_message(self, unused_client, unused_userdata, message):
        payload = message.payload
        # print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(
            # payload, message.topic, str(message.qos)))
        if not payload:
            return
        data = json.loads(payload)
        self.on_handle_message(data)

class DeviceClient(object):
    """Custom local client object"""
    def __init__(self, on_handle_message):
        print 'Creating device client'
        self.client = mqtt.Client(client_id=_CLIENT_ID)
        self.client.username_pw_set(username='unused', password=create_jwt())
        self.client.tls_set(ca_certs=root_cert_filepath)

        # Set all callback functions
        self.callback = ClientCallback(on_handle_message)
        self.client.on_connect = self.callback.on_connect
        self.client.on_publish = self.callback.on_publish
        self.client.on_disconnect = self.callback.on_disconnect
        self.client.on_subscribe = self.callback.on_subscribe
        self.client.on_message = self.callback.on_message

    def publish(self, payload):
        """Sends message to IoT Core"""
        self.client.publish(_MQTT_TOPIC, payload, qos=1)

    def begin(self):
        """Starts IoT core connection"""
        self.client.connect(_CLIENT_CONN_HOSTNAME, _CLIENT_CONN_PORT)
        self.client.subscribe(_MQTT_CONFIG_TOPIC, qos=1)
        self.client.loop_start()

    def stop(self):
        """Stops IoT core connection"""
        self.client.loop_stop()

