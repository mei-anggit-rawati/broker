
from paho import mqtt
import paho.mqtt.client as paho
import paho.mqtt.subscribe as subscribe
import ssl

def print_message(client, userdata, message):
    print('%s : %s' % (message.topic, message.payload))


# message = [{'topic' : 'mei/anggit/rawati', 'payload' : '123456789'}, {'mei/anggit/rawati', 'mey', 0, FALSE}]

sslSettings = ssl.SSLContext(mqtt.client.ssl.PROTOCOL_TLS)
auth = {'username': 'admin', 'password': 'Admin12345'}
subscribe.callback(print_message, '#', hostname='0ef562581d144a8da051382a90237387.s1.eu.hivemq.cloud', port=8883, auth=auth, tls=sslSettings, protocol=paho.MQTTv31)
