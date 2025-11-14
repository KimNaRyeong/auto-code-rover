Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
from django.forms import Media
import datetime
import traceback
import sys

def create_media(MediaClass):
    '''Creates a simple Media object with only one or two items.'''
    return MediaClass(css={'all': ['main.css']}, js=['main.js'])

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

start = datetime.datetime.now()
media = create_media(Media)
for i in range(100000):
    media = media + create_media(Media)

end_time = datetime.datetime.now() - start
if end_time.total_seconds() > 60:  # if it takes more than 1 minute
    raise AssertionError("Media.__add__ is slow")

print('100000 additions took:', end_time)
```
This script creates a `Media` object and adds to it 100,000 times. It then checks if the operation took more than 1 minute. If it did, it raises an `AssertionError` with a stack trace of the issue. If not, it prints the time taken for the operation and exits with code 0.

You can run this script by executing `python3 reproducer.py` in your terminal.