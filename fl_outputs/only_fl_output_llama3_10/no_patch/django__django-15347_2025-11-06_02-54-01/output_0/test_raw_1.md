Here is the reproducer script:

```python
import django
from django.contrib.messages.storage.base import Message
from django.contrib.messages.storage.cookie import MessageEncoder, MessageDecoder
import traceback
import sys

def print_stacktrace(e: Exception):
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
        settings = {}
        django.setup()
        original_message = Message(10, "Here is a message", extra_tags="")
        encoder = MessageEncoder()
        encoded_message = encoder.encode(original_message)
        decoder = MessageDecoder()
        decoded_message = decoder.decode(encoded_message)
        assert original_message.extra_tags == ""
        assert decoded_message.extra_tags == "", "Extra tags should still be an empty string after serialization and deserialization"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        exit(0)

if __name__ == "__main__":
    main()
```

This script sets up a Django environment, creates a message with empty extra tags, serializes and deserializes the message using the `MessageEncoder` and `MessageDecoder`, and then asserts that the extra tags are still an empty string after deserialization. If the assertion fails, it prints the stack trace and raises an exception.