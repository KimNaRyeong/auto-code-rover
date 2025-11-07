Here is the reproducer script:

```python
import django
from django.contrib.messages.storage.base import Message
from django.contrib.messages.storage.cookie import MessageEncoder, MessageDecoder

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
        settings = django.conf.settings.configure()
        original_message = Message(10, "Here is a message", extra_tags="")
        encoded_message = MessageEncoder().encode(original_message)
        decoded_message = MessageDecoder().decode(encoded_message)
        if not isinstance(decoded_message.extra_tags, str) or decoded_message.extra_tags == "":
            raise AssertionError("Expected extra_tags to be an empty string")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script sets up the Django environment and then serializes and deserializes a message with `extra_tags` set to an empty string. If the deserialized `extra_tags` is not an empty string or is `None`, it raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of any exceptions that occur during execution.