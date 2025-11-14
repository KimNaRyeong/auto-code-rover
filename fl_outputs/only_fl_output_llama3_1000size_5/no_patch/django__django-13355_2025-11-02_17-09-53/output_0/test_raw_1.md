Here is the reproducer script in a code block:

```python
import datetime
from django.forms import Media
import sys

def create_media(MediaClass):
    return MediaClass(css={'all': ['main.css']}, js=['main.js'])

start = datetime.datetime.now()
media = create_media(Media)
for i in range(100000):
    media = media + create_media(Media)

try:
    for i in range(100001):
        media = media + create_media(Media)
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

print('100000 additions took: %s' % (datetime.datetime.now() - start))
```

This script will reproduce the issue by adding a large number of `Media` objects to each other. If the performance becomes terrible, it will raise an `AssertionError` and print the stack trace.