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
    if not isinstance(decoded_message.extra_tags, str) or decoded_message.extra_tags:
        raise AssertionError("extra_tags should be an empty string")
    print_stacktrace(Exception("Issue reproduced"))

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present. Exiting with code 0.")
        exit(0)
```

This script sets up the Django environment, creates a message object with empty extra_tags, encodes and decodes it using the MessageEncoder and MessageDecoder, and then checks if the decoded extra_tags is still an empty string. If it's not, it raises an AssertionError and prints the stack trace.