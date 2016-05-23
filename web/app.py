"""Main Flask app for median-microservice."""
from datetime import datetime, timedelta
from os import environ
from time import mktime

from flask import Flask, jsonify, request, url_for
from rq import Queue
from rq.exceptions import NoSuchJobError
from rq.job import Job

from tasks import calculate_median
from worker import redis_conn

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(
    environ.get('FLASK_SETTINGS', 'config.DevConfig')
)

q = Queue(connection=redis_conn)


@app.route('/put', methods=['POST', 'PUT'])
def put():
    """
    Receive an integer, store it in redis.

    Expects a JSON object on PUT/POST in the following format:

    {
        'int': <integer>
    }

    Keys are unix timestamps of when they were stored in redis.
    """
    try:
        put_int = int(request.form.get('int'))
    except ValueError:
        return jsonify({
            "message": "'int' must be a valid integer."
        }), 422
    now = datetime.now()
    key = int(mktime(now.timetuple()))
    redis_conn.rpush(key, put_int)
    redis_conn.expire(key, 3600)  # Expire this key in one hour.
    expires = now + timedelta(minutes=1)
    return jsonify({
        "integer_received": put_int,
        "expires": int(mktime(expires.timetuple()))
    })


@app.route('/median', methods=['GET'])
def median():
    """
    Initiate a median calculation for all integers stored in the last minute.

    Returns a JSON object in the following format:
    {
        "job_id": {job_id},
        "url": {url_where_result_will_be_returned}
    }
    """
    job = q.enqueue_call(
        func=calculate_median,
        args=(datetime.now(),),
        kwargs={'minutes': 1},
        result_ttl=5000
    )
    job_id = job.get_id()
    return jsonify({
        "job_id": job_id,
        "url": url_for('median_request_results', job_id=job_id, _external=True)
    })


@app.route("/median-results/<job_id>", methods=['GET'])
def median_request_results(job_id):
    """
    Return results of a median calculation request.

    HTTP 200: If calculation is complete. Response JSON object format:
    {
        "message": "Calculation complete!",
        "median": {calculated_median}
    }

    HTTP 202: If calculation is not-yet complete. Response JSON object format:
    {
        "message": "Still processing..."
    }
    """
    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except NoSuchJobError:
        return jsonify({
            "message": "No job exists with ID: {}".format(job_id)
        }), 404
    else:
        if job.is_finished:
            result_dict = jsonify({
                "message": "Calculation complete!",
                "median": job.result
            })
            return result_dict, 200
        else:
            return jsonify({
                "message": "Still processing..."
            }), 202

if __name__ == '__main__':  # pragma: no cover
    app.run()
