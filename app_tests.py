"""Tests for median-microservice."""
import time
import unittest

from flask import json
from rq import Connection, Queue, SimpleWorker

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
        median_not_finished_job_req = self.app.get(
            '/median-results/{}'.format(median_as_dict['job_id'])
        )
        assert median_not_finished_job_req.status_code == 202
        not_finished_as_dict = json.loads(median_not_finished_job_req.data)
        assert not_finished_as_dict['message'] == (
            "Still processing..."
        )
        time.sleep(1)
        with Connection(redis_conn):
            queue = Queue(connection=redis_conn)
            worker = SimpleWorker([queue])
            worker.work(burst=True)

        median_job_req = self.app.get(
            '/median-results/{}'.format(median_as_dict['job_id'])
        )
        results_as_dict = json.loads(median_job_req.data)
        assert results_as_dict['median'] == 5


if __name__ == '__main__':
    unittest.main()
