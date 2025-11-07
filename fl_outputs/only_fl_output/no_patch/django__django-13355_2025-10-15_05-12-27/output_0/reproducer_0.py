# reproducer.py
import datetime
from django.forms import Media

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

def test_performance_issue():
    start = datetime.datetime.now()
    media = create_media(Media)
    try:
        for i in range(100000):
            media = media + create_media(Media)
        
        duration = datetime.datetime.now() - start
        # Insert an assertion that would realistically only pass if the issue was fixed.
        # Since we can't predict future performance improvements, this simply ensures
        # the issue presents as described: performance drop with the original approach.
        assert duration < datetime.timedelta(seconds=10), "Operation took too long, indicating a performance issue."
    except AssertionError as e:
        print_stacktrace(e)
        raise

def main():
    try:
        test_performance_issue()
    except AssertionError:
        exit(1)  # Exit with an error code if the issue is present.
    print("Issue not detected, operation completed within reasonable time.")
    exit(0)

if __name__ == '__main__':
    main()
