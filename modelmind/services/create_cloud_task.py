import datetime
import json
from typing import Dict, Optional

from google.cloud.tasks_v2 import CloudTasksAsyncClient, CreateTaskRequest, HttpMethod, HttpRequest, Task
from google.protobuf import duration_pb2, timestamp_pb2


async def create_task(
    client: CloudTasksAsyncClient,
    json_payload: Dict,
    project: str,
    location: str,
    queue: str,
    url: str,
    scheduled_seconds_from_now: Optional[int] = None,
    task_id: Optional[str] = None,
    deadline_in_seconds: Optional[int] = None,
    body_as_url_params: bool = False,
    headers: Optional[Dict[str, str]] = None,
) -> Task:
    """Create an HTTP POST task with a JSON payload.
    Args:
        client: The Cloud Tasks client.
        project: The project ID where the queue is located.
        location: The location where the queue is located.
        queue: The ID of the queue to add the task to.
        url: The target URL of the task.
        json_payload: The JSON payload to send.
        scheduled_seconds_from_now: Seconds from now to schedule the task for.
        task_id: ID to use for the newly created task.
        deadline_in_seconds: The deadline in seconds for task.
    Returns:
        The newly created task.
    """

    # Construct the task.
    task = Task(
        http_request=HttpRequest(
            http_method=HttpMethod.POST,
            url=url,
            headers=headers,
            body=json.dumps(json_payload).encode() if not body_as_url_params else None,
        ),
        name=(client.task_path(project, location, queue, task_id) if task_id is not None else None),
    )

    # Convert "seconds from now" to an absolute Protobuf Timestamp
    if scheduled_seconds_from_now is not None:
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(datetime.datetime.utcnow() + datetime.timedelta(seconds=scheduled_seconds_from_now))
        task.schedule_time = timestamp

    # Convert "deadline in seconds" to a Protobuf Duration
    if deadline_in_seconds is not None:
        duration = duration_pb2.Duration()
        duration.FromSeconds(deadline_in_seconds)
        task.dispatch_deadline = duration

    return await client.create_task(
        CreateTaskRequest(
            # The queue to add the task to
            parent=client.queue_path(project, location, queue),
            # The task itself
            task=task,
        )
    )
