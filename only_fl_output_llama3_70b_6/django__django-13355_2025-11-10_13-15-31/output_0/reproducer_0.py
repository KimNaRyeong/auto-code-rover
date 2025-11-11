from django.forms import Media
import datetime
import traceback
import sys

def create_media(MediaClass):
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

def test_media_performance():
    start = datetime.datetime.now()
    media = create_media(Media)
    for i in range(100000):
        media = media + create_media(Media)
    
    end = datetime.datetime.now()
    duration = (end - start).total_seconds()
    if duration > 60:  # more than 1 minute
        raise AssertionError(f"Media.__add__ took too long ({duration:.2f} seconds)")
    print("Media.__add__ performance is acceptable")

if __name__ == "__main__":
    try:
        test_media_performance()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
