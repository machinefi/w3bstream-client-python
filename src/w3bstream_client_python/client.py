import datetime
import queue
import threading
import time
import sys
import json
import datetime

import requests
from typeguard import typechecked


@typechecked
class Header:
    def __init__(self, device_id: str, event_type: str = 'DEFAULT', timestamp: datetime.datetime = datetime.datetime.utcnow()):
        self.event_type = event_type
        self.device_id = device_id
        self.timestamp = timestamp


PUBLISH_INTERVAL = 5
PUBLISH_BATCH_SIZE = 10
_DATA_PUSH_EVENT_TYPE = "DA-TA_PU-SH"


@typechecked
class Client:
    def __init__(self, url: str, api_key: str, queue_size: int = 0):
        self.url = url
        self.api_key = api_key
        self.queue = queue.Queue(queue_size)
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def publish_event_sync(self, header: Header, payload: bytes) -> requests.Response:
        """
        Publishes an event synchronously.
        """
        body = [{
            'device_id': header.device_id,
            'event_type': header.event_type,
            'payload': payload.decode('utf-8'),
            'timestamp':  int(round(header.timestamp.timestamp())),
        }]
        return self._publish_event(body)

    def publish_event(self, header: Header, payload: bytes) -> bool:
        """
        Publishes an event asynchronously.

        No callback is provided because the event is added to a queue and published in batches.
        If encountering errors when publishing, response body will be printed to stderr.

        Returns:
            True if the event was successfully added to the queue, False otherwise.
        """
        try:
            self.queue.put_nowait((header, payload))
            return True
        except queue.Full:
            sys.stderr.write(
                "the queue is full when publishing the data to W3bstream")
            return False

    def _worker(self):
        while True:
            # fetch events
            events = []
            for header, payload in self._fetch_event_batch():
                events.append({
                    'device_id': header.device_id,
                    'event_type': header.event_type,
                    'payload': payload.decode('utf-8'),
                    'timestamp':  int(round(header.timestamp.timestamp())),
                })
            # publish events
            resp = self._publish_event(events)
            if resp.status_code >= 400:
                # TODO: Support retry mechanism when failed to publish
                sys.stderr.write(
                    "an error occurred when publishing the data to W3bstream: status_code %d, body: %s" % (resp.status_code, resp.text))
            # sleep interval
            time.sleep(PUBLISH_INTERVAL)

    def _fetch_event_batch(self):
        """
        Fetches a batch of events from the queue.

        Fetches up to PUBLISH_BATCH_SIZE events from the queue.
        It will block until at least one event is available.
        """
        count = 0
        while count < PUBLISH_BATCH_SIZE:
            try:
                if count == 0:
                    yield self.queue.get()
                else:
                    yield self.queue.get_nowait()
                count += 1
            except queue.Empty:
                break

    def _publish_event(self, events: list) -> requests.Response:
        headers = {
            'Authorization': 'Bearer ' + self.api_key,
            'Content-Type': 'application/octet-stream',
        }
        timestamp = int(round(datetime.datetime.now().timestamp()))
        url = f"{self.url}?eventType={_DATA_PUSH_EVENT_TYPE}&timestamp={timestamp}"
        data_bytes = json.dumps(events)
        return requests.post(url, data=data_bytes,  headers=headers)
