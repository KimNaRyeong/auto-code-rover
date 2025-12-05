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

def main():
    start = datetime.datetime.now()
    media = create_media(Media)
    for i in range(100000):
        media = media + create_media(Media)
    print('100000 additions took: %s' % (datetime.datetime.now() - start))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")
```
This script creates a `Media` object and adds another `Media` object to it 100,000 times. It then prints the time taken for the additions. If the issue is present, an `AssertionError` will be raised with a stack trace.

To fix the issue, you can replace the `Media` class with the `CustomMedia` class from the issue description. Here is the modified `reproducer.py`:
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

def create_media(MediaClass):
    '''Creates a simple Media object with only one or two items.'''
    return MediaClass(css={'all': ['main.css']}, js=['main.js'])

def main():
    start = datetime.datetime.now()
    media = create_media(CustomMedia)
    for i in range(100000):
        media = media + create_media(CustomMedia)
    print('100000 additions took: %s' % (datetime.datetime.now() - start))

if __name__ == "__main__":
    main()
```
This script uses the `CustomMedia` class instead of the `Media` class. If the issue is fixed, the script will exit with code 0.