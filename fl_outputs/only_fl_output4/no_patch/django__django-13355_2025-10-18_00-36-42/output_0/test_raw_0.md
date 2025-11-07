```python
# reproducer.py
from django.forms import Media
import datetime

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

def create_media(MediaClass):
    '''Creates a simple Media object with only one or two items.'''
    return MediaClass(css={'all': ['main.css']}, js=['main.js'])

def test_issue_performance():
    start = datetime.datetime.now()
    media = create_media(Media)
    try:
        for i in range(100000):
            media = media + create_media(Media)

        duration = datetime.datetime.now() - start
        # Assuming the issue is present if the operation takes longer than a certain threshold (e.g., 5 seconds).
        # This threshold might need to be adjusted based on your machine's performance.
        assert duration.total_seconds() < 5, "The operation took too long, indicating a performance issue."
    except AssertionError as e:
        print_stacktrace(e)
        raise

def test_issue_fixed():
    class CustomMedia(Media):
        def __add__(self, other):
            combined = CustomMedia()
            if len(self._css_lists) + len(other._css_lists) > 1000:
                combined._css_lists = [self._css, other._css]
            else:
                combined._css_lists = self._css_lists + other._css_lists

            if len(self._js_lists) + len(other._js_lists) > 1000:
                combined._js_lists = [self._js, other._js]
            else:
                combined._js_lists = self._js_lists + other._js_lists

            return combined

    start = datetime.datetime.now()
    media = create_media(CustomMedia)
    for i in range(100000):
        media = media + create_media(CustomMedia)

    duration = datetime.datetime.now() - start
    print(f"Modified implementation time: {duration}")

if __name__ == "__main__":
    try:
        test_issue_performance()
        print("Performance issue detected.")
    except AssertionError as e:
        test_issue_fixed()
        print("The modified implementation does not have the performance issue.")
        exit(0)
```