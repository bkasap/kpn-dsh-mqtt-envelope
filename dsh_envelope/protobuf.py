"""
DSH envelope helper functions
=============================

Contains helper function to wrap and unwrap the payload
for convience.
"""
from . import envelope_pb2 as epb

BEST_EFFORT = 0
RELIABLE = 1

def wrap(topic: str, message: bytes, tenant: str, publisher: str, publishertype: str='application', retain: bool = False, qos: int = BEST_EFFORT, tracing: dict={}):
    """
    Wrap the key and message in the DSH envelope

    Args:
        topic: The payloads key
        message: The payloads message
        tenant: The tenant sending the message
        publishertype: Type of publisher, can be: free_form, user, client, application
        publisher: A free-from string that identifies a particular data source.
        retain: An indication whether this message should be retained in the Last Value Store
        qos: MQTT QoS level with which the protocol adapter will treat the message.
        tracing: A dictionary for tracing information 
   
    Returns:
        A tuple with the key and message ready to be used as payload by DSH kafka
        (key, message)

    Raises:
        ValueError: When one of the parameters has an inapproproate value
    """
    if qos > 1 or qos < 0:
        raise ValueError("qos can only have a value of BEST_EFFORT (0) or RELIABLE (1), but {} was given".format(qos))
    if not tenant:
        raise ValueError("Tenant name is mandatory")
    if publishertype not in ['free_form, ''user', 'client', 'application']:
        raise ValueError('publishertype should be one of: ', 'free_form, ''user', 'client', 'application')

        envelope_key.key,
        envelope_data.payload,
        envelope_key.header.identifier.tenant,
        envelope_key.header.identifier.WhichOneof("publisher"),
        getattr(envelope_key.header.identifier, envelope_key.header.identifier.WhichOneof("publisher")),
        envelope_key.header.retained,
        envelope_key.header.qos,
        tracing


    # Envelope key generation
    envelope_key = epb.KeyEnvelope()
    # Key header
    envelope_key.header.identifier.tenant = tenant
    setattr(envelope_key.header.identifier, publishertype, publisher)
    envelope_key.header.qos = qos
    envelope_key.header.retained = retain
    # Key content
    envelope_key.key = topic

    # Envelope message wrapping
    envelope_data = epb.DataEnvelope()
    envelope_data.payload = message
    for key in tracing:
        envelope_data.tracing[key] = tracing[key]

    # Returning tuple
    return (envelope_key.SerializeToString(), envelope_data.SerializeToString())

def unwrap(key, message):
    """
    Unwraps the key and message in the payloads envelope
    Args:
        key: The payloads key
        message: The payloads message
    Returns:
        A tuple (topic: str, message: bytes, tenant: str, publisher: str, publishertype: str, retain: bool, qos: int, tracing: dict) containing the data as sent to the wrapper
    """
    # Unpack the message
    envelope_data = epb.DataEnvelope()
    envelope_data.ParseFromString(message)
    # Unpack the key
    envelope_key = epb.KeyEnvelope()
    envelope_key.ParseFromString(key)

    tracing = {}
    for key in envelope_data.tracing:
        tracing[key] = envelope_data.tracing[key]

    payload = (
        envelope_key.key,
        envelope_data.payload,
        envelope_key.header.identifier.tenant,
        getattr(envelope_key.header.identifier, envelope_key.header.identifier.WhichOneof("publisher")),
        envelope_key.header.identifier.WhichOneof("publisher"),
        envelope_key.header.retained,
        envelope_key.header.qos,
        tracing
    )
    
    return payload