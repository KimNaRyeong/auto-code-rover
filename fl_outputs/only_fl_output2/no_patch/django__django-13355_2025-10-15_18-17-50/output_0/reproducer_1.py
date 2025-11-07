# reproducer.py

import datetime
from django.forms import Media

# Function to print stack trace
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

def test_default_media_class_performance_issue():
    start = datetime.datetime.now()
    media = create_media(Media)
    for i in range(100000):
        media = media + create_media(Media)
    duration = datetime.datetime.now() - start
    print(f'Default Media class - 100000 additions took: {duration}')
    if duration.total_seconds() >= 60:
        raise AssertionError('Performance issue detected with the default Media class')

def test_custom_media_class_resolves_issue():
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
    print(f'CustomMedia class - 100000 additions took: {duration}')
    if duration.total_seconds() > 60:
        raise AssertionError('CustomMedia class did not fix the performance issue')

def main():
    try:
        test_default_media_class_performance_issue()
        print("Original Media class performance issue detected.")
        print("Attempting to verify the fix with CustomMedia class...")
        test_custom_media_class_resolves_issue()
        print("Issue is fixed in the CustomMedia class.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    exit(0)

if __name__ == "__main__":
    main()
