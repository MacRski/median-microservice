"""Tests for median-microservice worker.py."""
import unittest

from flask import json

from app import app as microservice
from worker import redis_conn


class MedianMicroServiceWorkerTestCase(unittest.TestCase):
    """Tests the median-microservice worker.py module."""

    def setUp(self):
        """Setup the test client."""
        self.app = microservice.test_client()

    def test_median_calculation(self):
        """Test the /median-results/<job_id> endpoint."""
        job_id = redis_conn.get('TEST_JOB_ID')
        median_job_req = self.app.get(
            '/median-results/{}'.format(job_id)
        )
        results_as_dict = json.loads(median_job_req.data)
        assert results_as_dict['median'] == 5

if __name__ == '__main__':
    unittest.main()
