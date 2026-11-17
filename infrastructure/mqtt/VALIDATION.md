# MQTT infrastructure validation

Executed on 2026-11-17 on an Apple Silicon Mac using Colima and Docker.

## Environment

- Colima 0.10.3 (Apple Virtualization Framework)
- Docker CLI 29.8.1; Docker Compose 5.5.1
- Broker: `eclipse-mosquitto:2.0.22`
- Pulled broker digest: `sha256:81a6193ae693942a3231cd3ac52875b02b7e3a19da671b2fb4b55cc874c5b279`
- Integration client: Python 3.12 with paho-mqtt 2.1.0

## Observed results

| Check | Result |
| --- | --- |
| Shell/Python syntax and Compose validation | Passed |
| Setup creates local credentials and certificates | Passed |
| Broker startup and authenticated health check | Healthy |
| Anonymous connection | Rejected |
| Incorrect password | Rejected |
| Verified TLS + QoS 1 publish/subscribe | Passed; received payload matched sent payload |
| Device publishes to another device's topic | Rejected |
| Backend publishes telemetry | Rejected |
| Write-only device subscribes to telemetry | No unauthorized delivery |
| Broker restart and readiness recovery | Healthy |
| Host connection to localhost:8883 with CA/hostname validation | Passed; TLS 1.2 negotiated |
| Git excludes generated credentials and private keys | Passed |

Integration test output:

```text
PASS: anonymous and invalid-password connections rejected
PASS: authenticated TLS QoS 1 telemetry round-trip
PASS: cross-device and backend publishing rejected by ACL
PASS: write-only device cannot read telemetry
ALL MQTT CHECKS PASSED
```

The broker was left running at the end of validation. No Azure/cloud resources were provisioned. Real ESP32 hardware, a production backend consumer, long-duration operation, and durable offline delivery were not tested.
