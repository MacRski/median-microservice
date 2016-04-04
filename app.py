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


@app.route('/put/<int:put_int>', methods=['GET'])
def put(put_int):
    """
    Receive an integer, store it in redis.

    Integers are stored in redis as keys in the following format: 'int:{int}'.
    Values of each key are the amount of times that integer was 'put'.
    Keys expire after a minute.
    """
    redis_key = "int:{}".format(put_int)
    if redis_conn.get(redis_key):
        redis_conn.incr(redis_key)
    else:
        redis_conn.setex("int:{}".format(put_int), 1, 60)
    expires = datetime.datetime.now() + datetime.timedelta(minutes=1)
    return jsonify({
        "integer_received": put_int,
        "expires": time.mktime(expires.timetuple())
    })


@app.route('/median', methods=['GET'])
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
    """Return results of a median calculation request."""
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
