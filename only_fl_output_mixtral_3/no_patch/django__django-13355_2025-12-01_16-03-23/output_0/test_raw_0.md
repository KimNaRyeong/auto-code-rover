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

if (datetime.datetime.now() - start).total_seconds() > 5:
    raise AssertionError("Performance issue found")

print('100000 additions took: %s' % (datetime.datetime.now() - start))
```
The script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will exit with code 0 when the issue is fixed.

You can run the script by executing `python3 reproducer.py` in the terminal.

You can also test the modified Media class by replacing the `create_media` function with the following:
```python
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
```
This should run in under a second and not raise an `AssertionError`.