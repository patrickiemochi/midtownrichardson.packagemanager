import os
import tempfile
import unittest
import json

import app


class HotelAPITest(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.DB_NAME = tempfile.mkstemp()
        app.init_db()
        self.client = app.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.DB_NAME)

    def test_room_creation_and_reservation(self):
        # Create room
        response = self.client.post('/rooms', json={'number': '101', 'type': 'single', 'price': 100})
        self.assertEqual(response.status_code, 201)
        room_id = response.get_json()['id']

        # Check availability before booking
        response = self.client.get(f'/rooms/{room_id}/availability?check_in=2024-01-01&check_out=2024-01-02')
        self.assertTrue(response.get_json()['available'])

        # Create reservation
        response = self.client.post('/reservations', json={
            'room_id': room_id,
            'guest_name': 'Alice',
            'check_in': '2024-01-01',
            'check_out': '2024-01-02'
        })
        self.assertEqual(response.status_code, 201)

        # Check availability after booking
        response = self.client.get(f'/rooms/{room_id}/availability?check_in=2024-01-01&check_out=2024-01-02')
        self.assertFalse(response.get_json()['available'])


if __name__ == '__main__':
    unittest.main()
