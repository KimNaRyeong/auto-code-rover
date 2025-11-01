Here is the reproducer script:

```python
import django
from django.contrib.messages.storage.base import Message
from django.contrib.messages.storage.cookie import MessageEncoder, MessageDecoder
from django.conf import settings

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

def main():
    settings.configure()
    original_message = Message(10, "Here is a message", extra_tags="")
    encoded_message = MessageEncoder().encode(original_message)
    decoded_message = MessageDecoder().decode(encoded_message)
    if not isinstance(decoded_message.extra_tags, str) or decoded_message.extra_tags == "":
        raise AssertionError("Issue present")
    print("Issue fixed")

try:
    main()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue fixed")
    exit(0)
```

This script will run the reproducer and if the issue is present, it will raise an `AssertionError` with a stack trace. If the issue is not present (i.e., the extra_tags are correctly serialized and deserialized), it will print "Issue fixed" and exit with code 0.

Please note that this script should be run in a Django project environment where settings are configured.