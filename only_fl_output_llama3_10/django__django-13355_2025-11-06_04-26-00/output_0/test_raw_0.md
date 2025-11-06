Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import datetime
from django.forms import Media

def create_media(MediaClass):
    return MediaClass(css={'all': ['main.css']}, js=['main.js'])

start = datetime.datetime.now()
media = create_media(Media)
for i in range(100000):
    media = media + create_media(Media)

try:
    # Add some more to see if the issue persists
    for _ in range(10):
        media = media + create_media(Media)
except Exception as e:
    print_stacktrace(e)
    raise

print('100000 additions took: %s' % (datetime.datetime.now() - start))
```

This script creates a `Media` object and adds 100,000 more of the same type using the `+` operator. If the issue is present, it will raise an exception and print the stack trace.