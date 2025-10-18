# reproducer.py
import datetime
from django.forms import Media

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

def test_performance():
    start = datetime.datetime.now()
    media = create_media(Media)
    for i in range(100000):
        media = media + create_media(Media)
    duration = datetime.datetime.now() - start
    print(f'100000 additions took: {duration}')
    # Assuming any duration longer than 5 seconds is indicative of the performance issue
    assert duration < datetime.timedelta(seconds=5), "Performance degradation detected"

def main():
    try:
        test_performance()
    except AssertionError as e:
        print_stacktrace(e)
        raise e
    print("No performance issues detected.")

if __name__ == "__main__":
    main()
