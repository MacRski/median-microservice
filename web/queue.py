"""median-microservice Redis queue."""
import os

import redis

from flask import Blueprint, jsonify
from rq import Queue
from rq.exceptions import NoSuchJobError
from rq.job import Job

redis_url = os.environ.get('REDISTOGO_URL', 'redis://redis')

redis_conn = redis.from_url(redis_url)

task_queue = Queue(connection=redis_conn)

task_detail_routes = Blueprint('task_detail_routes', __name__)


@task_detail_routes.route("/tasks/<task_id>", methods=['GET'])
def task_detail(task_id):
    """
    Return results of a queueable task request.

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
        job = Job.fetch(task_id, connection=redis_conn)
    except NoSuchJobError:
        return jsonify({
            "message": "No task exists with ID: {}".format(task_id)
        }), 404
    else:
        if job.is_finished:
            result_dict = jsonify({
                "message": "Calculation complete!",
                "task_results": job.result
            })
            return result_dict, 200
        else:
            return jsonify({
                "message": "Still processing..."
            }), 202
