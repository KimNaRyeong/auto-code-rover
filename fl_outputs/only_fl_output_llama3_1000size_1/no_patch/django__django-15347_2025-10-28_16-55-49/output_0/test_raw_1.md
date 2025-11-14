Here is the reproducer script:

```python
import django
from django.contrib.messages.storage.base import Message
from django.contrib.messages.storage.cookie import MessageEncoder, MessageDecoder
from django.conf import settings

def main():
    try:
        settings.configure()  # Just to allow the following import
        original_message = Message(10, "Here is a message", extra_tags="")
        encoded_message = MessageEncoder().encode(original_message)
        decoded_message = MessageDecoder().decode(encoded_message)
        assert original_message.extra_tags == ""
        assert decoded_message.extra_tags == ""
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        print("Issue not present. Exiting with code 0.")
        exit(0)

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

if __name__ == "__main__":
    main()
```

This script sets up the Django environment, creates a message with empty extra_tags, encodes and decodes it using the MessageEncoder and MessageDecoder classes, and then asserts that the original and decoded messages have the same extra_tags. If the assertion fails (i.e., the issue is present), it prints the stack trace and raises an AssertionError. If the assertion passes (i.e., the issue is not present), it prints a message indicating that the issue was not found and exits with code 0.