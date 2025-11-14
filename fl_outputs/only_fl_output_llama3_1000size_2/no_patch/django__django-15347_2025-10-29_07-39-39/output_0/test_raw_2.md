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

def reproduce_issue():
    try:
        settings.configure()
        original_message = Message(10, "Here is a message", extra_tags="")
        encoded_message = MessageEncoder().encode(original_message)
        decoded_message = MessageDecoder().decode(encoded_message)
        assert original_message.extra_tags == ""
        assert not (decoded_message.extra_tags is None)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    settings.configure()
    reproduce_issue()
```

This script sets up the Django settings, creates a `Message` object with an empty `extra_tags`, encodes and decodes it using the `MessageEncoder` and `MessageDecoder`, and then asserts that the original message's `extra_tags` is still an empty string and the decoded message's `extra_tags` is not `None`. If either of these assertions fail, the script prints a stack trace and exits with code 1.