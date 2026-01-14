 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import queue
import threading
import time

def check_thread(wqueue):
    while True:
        url = wqueue.get()
        try:
            # Simulate a long-running task
            time.sleep(0.1)
        finally:
            wqueue.task_done()

if __name__ == "__main__":
    wqueue = queue.Queue()

    # Add some items to the queue
    for i in range(10):
        wqueue.put(i)

    # Start the worker thread
    worker = threading.Thread(target=check_thread, args=(wqueue,))
    worker.start()

    # Wait for all items to be processed
    wqueue.join()

    # Add more items to the queue after it has been joined
    for i in range(10, 20):
        wqueue.put(i)

    # This will raise a ValueError: task_done() called too many times
    wqueue.join()
```
To reproduce the issue, execute the script with `python3 reproducer.py`. The script simulates a long-running task in the worker thread and adds items to the queue after it has been joined, which leads to the `ValueError: task_done() called too many times` exception.

To fix the issue, you can add a check to see if the queue is still active before calling `task_done()`:
```python
def check_thread(wqueue):
    while True:
        url = wqueue.get()
        try:
            # Simulate a long-running task
            time.sleep(0.1)
        finally:
            if not wqueue.full():
                wqueue.task_done()
```
This modification ensures that `task_done()` is only called if the queue is not full, which prevents the `ValueError` exception.