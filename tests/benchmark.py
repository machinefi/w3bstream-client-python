import sys
import os
import timeit
import unittest
import time
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src/w3bstream_client_python'))

from client import Client, Header
import client

class TestClient(unittest.TestCase):
    def setUp(self):
        self.send_count = 0

    def qtest_publish_event_sync(self):
        header = Header(device_id='my-device-id', event_type='my-event-type')
        payload = b'my-payload'
        cases = [1, 10, 20, 30, 50, 100, 200, 300, 500, 800]
        for case in cases:
            t = timeit.Timer(lambda: self.client.publish_event_sync_n(header, payload, case))
            result = t.timeit(number=1)
            print(f'publish_event_sync_n({case})\t{result:.4f}')

    def test_publish_event_performance(self):
        header = Header(device_id='my-device-id', event_type='my-event-type')
        payload = b'my-payload'

        batch_sizes = [10, 30, 50, 100, 150, 200, 300, 500, 1000]
        batch_sizes.reverse()
        requests = [1, 10, 100, 1000]
        workers = [16] #[1, 2, 4, 8, 10, 16]
        workers.reverse()
        print('PUBLISH_BATCH_SIZE\tRequests\tWorkers\tTime\tAverage Time')
        for worker in workers:
            self.client = Client(url='https://devnet-prod.w3bstream.com/api/w3bapp/event/eth_0x042396f51b99a7b7a18968283257b791c5e17541_helloworld', api_key='w3b_MV8xNjkxNDY5NDk3X25sSCFTJ2BeWjlkcQ', worker=worker, callback_async=self.callback_async)
            self.client.publish_event(header, payload)
            self.wait_for_queue(1)
            for batch_size in batch_sizes:
                client.PUBLISH_BATCH_SIZE = batch_size
                for request in requests:
                    self.send_count = 0
                    t = timeit.Timer(lambda: self.client.publish_event(header, payload))
                    t.timeit(number=request)
                    t = timeit.Timer(lambda: self.wait_for_queue(request))
                    result = t.timeit(number=1)
                    print(f'{batch_size}\t\t\t{request}\t\t{worker}\t{result:.2f}\t{(result/request):.4f}')
    
    def wait_for_queue(self, count):
        while self.client.queue.qsize() > 0 or self.send_count < count:
            time.sleep(0.1)
    
    def callback_async(self, events, response):
        self.send_count += len(events)

if __name__ == '__main__':
    unittest.main()
