"""Tests for median-microservice."""
import time
import unittest

from flask import json

import app


class MedianMicroServiceTestCase(unittest.TestCase):
    """
    Tests for median-microservice.

    Before running tests be sure the redis queue consumer (worker.py)
    is running in a separate shell:

        $ python worker.py
    """

    def setUp(self):
        """Setup the test client."""
        self.app = app.app.test_client()

    def test_missing_job_id(self):
        """Test incorrect median result requests are handled correctly."""
        unavailable_job_req = self.app.get('/median-results/i-do-not-exist')
        assert unavailable_job_req.status_code == 404
        req_as_dict = json.loads(unavailable_job_req.data)
        assert req_as_dict['message'] == (
            "No job exists with ID: i-do-not-exist"
        )

    def test_microservice(self):
        """
        Test the microservice.

        NOTE: This test will fail if the redis queue consumer (worker.py)
        is not running simultaneously (see README.md for details).
        """
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
        median_job_req = self.app.get(
            '/median-results/{}'.format(median_as_dict['job_id'])
        )
        results_as_dict = json.loads(median_job_req.data)
        assert results_as_dict['median'] == 5


if __name__ == '__main__':
    unittest.main()
