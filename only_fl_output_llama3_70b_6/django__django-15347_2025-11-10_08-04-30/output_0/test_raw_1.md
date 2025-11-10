Here is the revised standalone Python file `reproducer.py` to reproduce the issue:
```
import sys
from django.conf import settings

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    settings.configure(debug=True)  # Configure Django settings
    
    from django.contrib.messages.storage.base import Message
    from django.contrib.messages.storage.cookie import MessageEncoder, MessageDecoder

    original_message = Message(10, "Here is a message", extra_tags="")
    encoded_message = MessageEncoder().encode(original_message)
    decoded_message = MessageDecoder().decode(encoded_message)

    try:
        assert original_message.extra_tags == "" and decoded_message.extra_tags == ""
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```
This script configures Django settings before importing the necessary modules, which should fix the `ImproperlyConfigured` error. It then reproduces the issue by encoding and decoding a message with an empty string as the `extra_tags`, and checks if the decoded message still has an empty string as the `extra_tags`. If not, it raises an `AssertionError` and prints a stack trace of the issue.