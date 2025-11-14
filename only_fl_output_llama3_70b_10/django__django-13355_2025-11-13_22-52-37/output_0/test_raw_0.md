Here is the `reproducer.py` file to reproduce the issue:
```
from django.forms import Media
import datetime
import time

def create_media(MediaClass):
    '''Creates a simple Media object with only one or two items.'''
    return MediaClass(css={'all': ['main.css']}, js=['main.js'])

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    start = datetime.datetime.now()
    media = create_media(Media)
    for i in range(100000):
        media = media + create_media(Media)
    
    end = datetime.datetime.now()
    duration = (end - start).total_seconds()
    if duration > 60:  # more than 1 minute
        raise AssertionError("Media.__add__ performance issue detected")
    print('100000 additions took: %s seconds' % duration)
except Exception as e:
    print_stacktrace(e)
```
<|start_header_id|>