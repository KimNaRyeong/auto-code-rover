# reproducer.py
import datetime
from django.forms import Media
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def create_media(MediaClass=Media):
    '''Creates a simple Media object with only one or two items.'''
    return MediaClass(css={'all': ['main.css']}, js=['main.js'])

def test_performance_issue():
    start = datetime.datetime.now()
    media = create_media()
    for i in range(100000):
        media = media + create_media()
    
    end = datetime.datetime.now()
    duration = end - start
    print(f'100000 additions took: {duration}')
    
    # Setting a rough threshold for performance issue
    # This threshold might need adjustment based on the specifics of the issue you're encountering
    threshold = datetime.timedelta(seconds=10)  # Example threshold, adjust based on actual acceptable performance
    if duration > threshold:
        raise AssertionError("Performance issue detected: Operation took too long.")

if __name__ == "__main__":
    try:
        test_performance_issue()
        print("No performance issue detected. Exiting with code 0.")
        sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
