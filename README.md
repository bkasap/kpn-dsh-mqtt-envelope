# kpn-dsh-mqtt-envelope

### Installation:

```
pip install kpn-dsh-mqtt-envelope
```

### Usage:

```py
...
# Import dsh_envelope
import dsh_envelope
...
# Deserialize the mqtt message from kafka consumer
(topic, message, tenant, publisher, publishertype, retain, qos, tracing) = dsh_envelope.unwrap(key, value)

# Serialize the mqtt fields into kafka producer
(key, value) = dsh_envelope.wrap(topic, message, tenant, publisher, publishertype, retain, qos, tracing)
```

where ```type(key)``` and ```type(value)``` are ```bytes``` as serialized/deserialized by DSH mqtt kafka bridge.

### Example:

For a ```kafka-python``` consumer:

```py
from kafka import KafkaConsumer, KafkaProducer

# Initiate consumer
consumer = KafkaConsumer(...)
# Subscribe to a stream with regex-pattern for <streamname>
consumer.subscribe(pattern='^stream\\.<streamname>\\.[^.]*')

for msg in consumer:
    (topic, message, tenant, publisher, publishertype, retain, qos, tracing) = dsh_envelope.unwrap(key, value)
```
will return serialized values of the fields:
```
topic: str
    mqtt topic suffix that the message is published to
message: bytes
    payload in bytes
tenant: str
    name of the tenant message is published from
publisher: str
    name of the publisher
publishertype: str
    type of the publisher
retain: bool
    if the message should be retained
    thus will be available in latest value store and through http-protocol-adapter
qos: int
    quality of service for mqtt
tracing: dict
    tracing span context in a python dictionary
```