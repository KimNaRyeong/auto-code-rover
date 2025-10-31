Here is the reproducer script:

```python
import django
from django.contrib.messages.storage.base import Message
from django.contrib.messages.storage.cookie import MessageEncoder, MessageDecoder
from unittest import main

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
    try:
        settings.configure()
        original_message = Message(10, "Here is a message", extra_tags="")
        encoded_message = MessageEncoder().encode(original_message)
        decoded_message = MessageDecoder().decode(encoded_message)
        assert original_message.extra_tags == ""
        assert decoded_message.extra_tags == ""
        if decoded_message.extra_tags is None:
            raise AssertionError("extra_tags was converted to None")
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        exit(0)

if __name__ == "__main__":
    main()
```

This script sets up the necessary Django settings and then serializes and deserializes a `Message` object with an empty string for `extra_tags`. It then checks that both the original and decoded messages have the same value for `extra_tags`, which should be an empty string. If this assertion fails, it prints the stack trace of the failure and raises an `AssertionError`.