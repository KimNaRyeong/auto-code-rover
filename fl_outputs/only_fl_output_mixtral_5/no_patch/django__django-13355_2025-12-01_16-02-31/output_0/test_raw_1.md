 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from django.forms import Media
import datetime

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def create_media(MediaClass):
    '''Creates a simple Media object with only one or two items.'''
    return MediaClass(css={'all': ['main.css']}, js=['main.js'])

start = datetime.datetime.now()
media = create_media(Media)
for i in range(100000):
    media = media + create_media(Media)

if (datetime.datetime.now() - start).total_seconds() > 1:
    assert False, "Original Media class took too long to execute"

class CustomMedia(Media):
    def __add__(self, other):
        combined = CustomMedia()
        if len(self._css_lists) + len(other._css_lists) > 1000:
            combined._css_lists = [self._css, other._css]
        else:
            combined._css_lists = self._css_lists + other._css_lists

        if len(self._js_lists) + len(other._js_lists) > 100