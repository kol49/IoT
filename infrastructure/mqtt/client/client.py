"""DesignSpace MQTT 5 simulator and integration checks (TLS + topic ACLs)."""
import json
import os
import sys
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
import paho.mqtt.client as mqtt

HOST = os.environ.get('MQTT_HOST', 'localhost')
TOPIC = 'designspace/workspaces/studio-01/devices/device-01/telemetry'
CREDS = json.loads(Path('/app/clients.json').read_text())


def connect(user=None, password=None, accepted=True):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                         client_id=f'designspace-{uuid.uuid4().hex[:12]}', protocol=mqtt.MQTTv5)
    client.tls_set(ca_certs='/app/ca.crt')
    if user:
        client.username_pw_set(user, CREDS[user] if password is None else password)
    ready = threading.Event()
    codes = []
    def on_connect(c, userdata, flags, reason, properties):
        codes.append(reason)
        ready.set()
    client.on_connect = on_connect
    client.connect(HOST, 8883, keepalive=30)
    client.loop_start()
    if not ready.wait(10):
        client.loop_stop()
        raise AssertionError('Timed out waiting for CONNACK')
    if codes[0].is_failure == accepted:
        close(client)
        raise AssertionError(f'Unexpected connection result: {codes[0]}')
    return client


def close(client):
    client.disconnect()
    client.loop_stop()


def sample():
    return json.dumps({'reading_id': str(uuid.uuid4()), 'device_id': 'device-01',
        'workspace_id': 'studio-01', 'measured_at': datetime.now(timezone.utc).isoformat(),
        'illuminance_lux': 520.0, 'temperature_c': 22.4, 'humidity_percent': 45.0,
        'simulated': True})


def publish(client, topic, payload, allowed=True):
    done = threading.Event()
    reasons = []
    def on_publish(c, userdata, mid, reason, properties):
        reasons.append(reason)
        done.set()
    client.on_publish = on_publish
    client.publish(topic, payload, qos=1, retain=False)
    assert done.wait(10), 'Missing PUBACK'
    assert reasons[0].is_failure != allowed, f'Unexpected PUBACK: {reasons[0]}'


def test():
    clients = []
    try:
        for user, password in ((None, None), ('device-01', 'incorrect-password')):
            c = connect(user, password, accepted=False)
            close(c)
        print('PASS: anonymous and invalid-password connections rejected')
        backend = connect('backend'); clients.append(backend)
        device = connect('device-01'); clients.append(device)
        subscribed = threading.Event()
        received = threading.Event()
        messages = []
        def on_subscribe(c, userdata, mid, reasons, properties):
            if all(not r.is_failure for r in reasons):
                subscribed.set()
        backend.on_subscribe = on_subscribe
        def on_message(c, userdata, msg):
            messages.append(msg.payload.decode())
            received.set()
        backend.on_message = on_message
        backend.subscribe(TOPIC, qos=1)
        assert subscribed.wait(10), 'Subscription not acknowledged'
        payload = sample()
        publish(device, TOPIC, payload)
        assert received.wait(10) and payload in messages, 'Telemetry did not reach backend'
        print('PASS: authenticated TLS QoS 1 telemetry round-trip')
        publish(device, TOPIC.replace('device-01', 'device-02'), payload, allowed=False)
        publish(backend, TOPIC, payload, allowed=False)
        print('PASS: cross-device and backend publishing rejected by ACL')
        # Mosquitto may accept a SUBSCRIBE filter yet suppress unauthorized delivery.
        # Prove denial by delivery, not by SUBACK alone.
        leaked = threading.Event()
        device.on_message = lambda *args: leaked.set()
        device_subscribed = threading.Event()
        device.on_subscribe = lambda *args: device_subscribed.set()
        device.subscribe(TOPIC, qos=1)
        assert device_subscribed.wait(10), 'Missing device SUBACK'
        publish(device, TOPIC, sample())
        assert not leaked.wait(2), 'Write-only device received telemetry'
        print('PASS: write-only device cannot read telemetry')
        print('ALL MQTT CHECKS PASSED')
    finally:
        for client in clients:
            close(client)


def simulate():
    client = connect('device-01')
    try:
        while True:
            payload = sample()
            publish(client, TOPIC, payload)
            print(payload)
            time.sleep(30)
    finally:
        close(client)


def listen():
    client = connect('backend')
    client.on_message = lambda c, u, m: print(m.topic, m.payload.decode())
    client.subscribe('designspace/workspaces/studio-01/devices/+/telemetry', qos=1)
    try:
        while True:
            time.sleep(1)
    finally:
        close(client)


if __name__ == '__main__':
    try:
        {'test': test, 'simulate': simulate, 'listen': listen}[sys.argv[1] if len(sys.argv)>1 else 'test']()
    except KeyboardInterrupt:
        pass
