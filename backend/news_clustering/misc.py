import json
import threading
from threading import Thread


def dedupe_list(articles):
    return list(set(articles))


def create_task(task_id, func, *args, **kwargs):
    """Create a thread."""
    task_id = str(task_id)
    kwargs.update({"task_id": task_id})

    task = check_thread_running(task_id)
    if task is None:
        task = Thread(
            name=task_id,
            target=func,
            args=args,
            kwargs=kwargs,
            daemon=True,
        )
        task.start()


def check_thread_running(task_id):
    """Return the current running thread if the task name matches."""
    for task in threading.enumerate():
        if task.name == task_id:
            return task


def json_dumps(data):
    return json.dumps(data)

def json_load(data):
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return eval(data)