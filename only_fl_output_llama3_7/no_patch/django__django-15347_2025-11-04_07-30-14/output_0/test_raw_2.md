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
    
    if not isinstance(decoded_message.extra_tags, str) or decoded_message.extra_tags != "":
        raise AssertionError("Extra tags should be an empty string")
    else:
        print("Issue fixed. Exiting with code 0.")
        exit(0)

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
```

This script sets up the necessary Django settings, creates a message object with empty extra tags, encodes and decodes it to reproduce the issue. If the decoded message's extra tags are not an empty string or if they are `None`, it raises an `AssertionError` which is caught and printed using the provided function.

Please note that you need to have Django installed in your Python environment for this script to work.