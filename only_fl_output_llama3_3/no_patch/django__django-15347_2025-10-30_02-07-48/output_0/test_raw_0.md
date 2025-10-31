Here is the reproducer script:

```python
import django
from django.contrib.messages.storage.base import Message
from django.contrib.messages.storage.cookie import MessageEncoder, MessageDecoder

def main():
    try:
        settings = django.conf.settings.configure()
        original_message = Message(10, "Here is a message", extra_tags="")
        encoder = MessageEncoder()
        encoded_message = encoder.encode(original_message)
        decoder = MessageDecoder()
        decoded_message = decoder.decode(encoded_message)
        assert original_message.extra_tags == "", f"Expected extra_tags to be an empty string but got {decoded_message.extra_tags}"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
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

This script sets up the Django settings, creates a message with empty extra_tags, encodes and decodes it using the MessageEncoder and MessageDecoder, and then asserts that the decoded message's extra_tags is still an empty string. If the assertion fails (i.e., the decoded message's extra_tags is not an empty string), it prints the stack trace of the failure and raises an AssertionError.