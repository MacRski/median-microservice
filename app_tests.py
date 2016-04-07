"""Tests for median-microservice."""
import time
import unittest

from flask import json

from app import app as microservice
from worker import redis_conn


class MedianMicroServiceTestCase(unittest.TestCase):
    """Tests for median-microservice."""

    def setUp(self):
        """Setup the test client."""
        self.app = microservice.test_client()

    def test_missing_job_id(self):
        """Test incorrect median result requests are handled correctly."""
        unavailable_job_req = self.app.get('/median-results/i-do-not-exist')
        assert unavailable_job_req.status_code == 404
        req_as_dict = json.loads(unavailable_job_req.data)
        assert req_as_dict['message'] == (
            "No job exists with ID: i-do-not-exist"
        )

    def test_microservice(self):
        """Test the microservice."""
        redis_conn.flushall()
        req_1 = self.app.get('/put/1')
        assert '"integer_received": 1' in req_1.data
        req_2 = self.app.get('/put/1')
        del req_2
        req_3 = self.app.get('/put/4')
        del req_3
        req_4 = self.app.get('/put/6')
        del req_4
        req_5 = self.app.get('/put/8')
        del req_5
        req_6 = self.app.get('/put/10')
        del req_6
        median_req = self.app.get('/median')
        median_as_dict = json.loads(median_req.data)
        time.sleep(1)
        # Set the job_id to redis for worker_tests.py
        redis_conn.set('TEST_JOB_ID', median_as_dict['job_id'])


if __name__ == '__main__':
    unittest.main()
