"""Main Flask app for median-microservice."""
from datetime import datetime, timedelta
from os import environ
from time import mktime

from flask import Flask, jsonify, request

from decorators import queueable_task_route
from queue import redis_conn, task_queue, task_detail_routes
from tasks import calculate_median

app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(task_detail_routes)
app.config.from_object(
    environ.get('FLASK_SETTINGS', 'config.DevConfig')
)


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
@queueable_task_route
def median():
    """
    Initiate a median calculation for all integers stored in the last minute.

    Returns a JSON object in the following format:
    {
        "task_id": {task_id},
        "url": {url_where_result_will_be_returned}
    }
    """
    return task_queue.enqueue_call(
        func=calculate_median,
        args=(datetime.now(),),
        kwargs={'minutes': 1},
        result_ttl=5000
    )

if __name__ == '__main__':  # pragma: no cover
    app.run()
