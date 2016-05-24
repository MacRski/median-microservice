"""median-microservice decorators."""
from functools import wraps
from flask import jsonify, url_for


def queueable_task_route(f):
    """A decorator for wrapping routes that initiate queueable tasks."""
    def wrapper():
        task = f()
        task_id = task.get_id()
        return jsonify({
            "task_id": task_id,
            "url": url_for(
                'task_detail_routes.task_detail',
                task_id=task_id,
                _external=True
            )
        })

    return wrapper


def queueable_task(f):
    """A decorator for queueable tasks."""
    @wraps(f)
    def inner(*args, **kwargs):
        task_result = f(*args, **kwargs)
        return {
            'task': f.__name__,
            'result': task_result
        }
    return inner
