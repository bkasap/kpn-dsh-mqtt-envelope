import envelope
import json
import unittest


class TestWrappingInput(unittest.TestCase):
    """Test input errors are handled as expected"""

    def test_tenant_required(self):
        """Test an exception is raised if tenant is passed incorectly"""
        # Tenant is None
        with self.assertRaises(ValueError):
            envelope.wrap('key', b'message', None)
        
        # Tenant is empty string
        with self.assertRaises(ValueError):
            envelope.wrap('key', b'message', '')

    def test_key_valid(self):
        """Test an exception is raised if key is not a string"""
        with self.assertRaises(TypeError):
            envelope.wrap(1, b'message', 'tenant')

    def test_qos_valid(self):
        """Test that the value of qos is valid"""
        with self.assertRaises(ValueError):
            envelope.wrap('key', b'message', 'tenant', qos=3)

    def test_publishertype_valid(self):
        """Test that the publishertype is valid"""
        with self.assertRaises(ValueError):
            envelope.wrap('key', b'message', 'tenant', publishertype='nonvalid')


class TestWrapping(unittest.TestCase):
    """Test that wrapping is as expected"""

    def test_wrapping(self):
        """Tests that wrapping happends"""
        payload = envelope.wrap('key', b'message', 'tenant')
        self.assertEqual(payload, (b'\n\n\n\x08\n\x06tenant\x12\x03key', b'\n\x07message'))

    def test_wrapping_json(self):
        """Test that a serilaized json can me wrapped"""
        data = {'key': 'value'}
        data = (json.dumps(data)).encode('utf-8')
        payload = envelope.wrap('key', data, 'tenant')
        self.assertEqual(payload, (b'\n\n\n\x08\n\x06tenant\x12\x03key', b'\n\x10{"key": "value"}'))

    def test_utf8_wrapping(self):
        """Test that utf-8 special chars are correctly handled"""
        payload = envelope.wrap('key', '✨'.encode('utf-8'), 'tenant')
        self.assertEqual(payload, (b'\n\n\n\x08\n\x06tenant\x12\x03key', b'\n\x03\xe2\x9c\xa8'))

class TestUnwrapping(unittest.TestCase):
    """Tests that unwraping is executed"""

    def test_unwrapping(self):
        """Unwrap a simple message"""
        unwrap = envelope.unwrap(b'\n\n\n\x08\n\x06tenant\x12\x03key', b'\n\x07message')
        self.assertEqual(unwrap[0],'key')
        self.assertEqual(unwrap[1], b'message')


class TestWrapAndUnwrap(unittest.TestCase):
    """Doing some end to end wrapping testing"""
    
    def test_wuw_basic(self):
        """Testing wrapping and unwrapping does not mutate the data"""
        key = 'message_key'
        message = b'Some sort of text message'
        tenant = 'default'
        
        # Wrapping
        payload = envelope.wrap(key, message, tenant)
        # Unwrapping
        unwrap = envelope.unwrap(payload[0], payload[1])

        self.assertEqual(key, unwrap[0])
        self.assertEqual(tenant, unwrap[2])
        self.assertEqual(message, unwrap[1])

    def test_publisher_maintained(self):
        """Test the the publisher field is correctly maintained"""
        key = 'key'
        message = b'message'
        tenant = 'tenant'
        publisher = 'Accelerate!'

        # Wrapping
        payload = envelope.wrap(key, message, tenant, publisher)
        # Unwrapping
        unwrap = envelope.unwrap(payload[0], payload[1])
        self.assertEqual(unwrap[3], publisher)

    def test_utf8_wrapping(self):
        """Test that utf-8 special chars are correctly handled"""
        message = '✨'

        msg_bytes = message.encode('utf-8')
        # Wrapping
        payload = envelope.wrap('key', msg_bytes,  'tenant')
        # Unwrapping
        unwrap = envelope.unwrap(payload[0], payload[1])
        msg = unwrap[1].decode('utf-8')
        self.assertEqual(message, msg)


if __name__ == '__main__':
    unittest.main()

