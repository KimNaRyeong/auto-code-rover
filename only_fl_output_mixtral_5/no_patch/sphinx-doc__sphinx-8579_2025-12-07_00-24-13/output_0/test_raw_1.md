 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import queue
import threading
import time

def check_thread(wqueue):
    while True:
        try:
            url = wqueue.get(timeout=1)
        except queue.Empty:
            continue

        # Simulate long-running task
        time.sleep(0.1)

        # This is the line that raises the ValueError
        wqueue.task_done()

def main():
    wqueue = queue.Queue()

    # Add some items to the queue
    for i in range(10):
        wqueue.put(i)

    # Start the worker thread
    worker = threading.Thread(target=check_thread, args=(wqueue,))
    worker.start()

    # Wait for all items to be processed
    wqueue.join()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue reproduced"
```
To reproduce the issue, run the script with Python 3.8.6:
```
$ python3 reproducer.py
```
This should print a stack trace and raise an `AssertionError`.

The issue is caused by a race condition between the worker thread and the main thread. The worker thread calls `wqueue.task_done()` before the main thread has called `wqueue.get()`, which raises a `ValueError`.

To fix the issue, you can add a check to make sure that the item has been removed from the queue before calling `wqueue.task_done()`. Here is an updated version of the `check_thread()` function that fixes the issue:
```python
def check_thread(wqueue):
    while True:
        try:
            url = wqueue.get(timeout=1)
        except queue.Empty:
            continue

        # Simulate long-running task
        time.sleep(0.1)

        # Check if the item has been removed from the queue
        if not wqueue.full():
            # This is the line that fixes the issue
            wqueue.task_done()
```
With this fix, the script should exit with code 0:
```
$ python3 reproducer.py
```