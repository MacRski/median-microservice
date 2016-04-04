"""Main Flask app for median-microservice."""
import datetime
import time

from flask import Flask, url_for
from flask import jsonify
from rq import Queue
from rq.job import Job

from tasks import calculate_median
from worker import redis_conn

app = Flask(__name__)
q = Queue(connection=redis_conn)


@app.route('/put/<int:put_int>')
def put(put_int):
    """
    Receive an integer, store it in redis.

    key: integer
    value: 1 (always)
    time expiry: 1 minute
    """
    redis_conn.setex("int:{}".format(put_int), 1, 60)
    expires = datetime.datetime.now() + datetime.timedelta(minutes=1)
    return jsonify({
        "integer_received": put_int,
        "expires": time.mktime(expires.timetuple())
    })


@app.route('/median')
def median():
    """Return the median for all the values sent to /put in the last minute."""
    job = q.enqueue_call(
        func=calculate_median, result_ttl=5000
    )
    job_id = job.get_id()
    return jsonify({
        "job_id": job_id,
        "url": url_for('median_request_results', job_id=job_id, _external=True)
    })


@app.route("/median-results/<job_id>", methods=['GET'])
def median_request_results(job_id):
    """Return."""
    job = Job.fetch(job_id, connection=redis_conn)
    if job.is_finished:
        result_dict = jsonify({
            "message": "Calculation complete!",
            "median_of_last_minute": job.result
        })
        return result_dict, 200
    else:
        return {
            "message": "Still processing..."
        }, 202

if __name__ == '__main__':
    app.run()
