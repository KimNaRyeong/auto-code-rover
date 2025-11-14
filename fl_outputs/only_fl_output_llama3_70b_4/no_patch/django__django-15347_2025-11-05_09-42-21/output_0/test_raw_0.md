Here is the `reproducer.py` file that reproduces the issue:
```
import sys
from django.conf import settings
from django.contrib.messages.storage.base import Message
from django.contrib.messages.storage.cookie import MessageEncoder, MessageDecoder

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
    settings.configure()
    
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
This script sets up a minimal Django environment, creates a `Message` object with an empty string for `extra_tags`, serializes it using the `MessageEncoder`, deserializes it using the `MessageDecoder`, and then checks if the `extra_tags` attribute is still an empty string. If not, it raises an `AssertionError` and prints the stack trace using the provided function.

When run with `python3 reproducer.py`, this script should raise an `AssertionError` and print a stack trace when the issue is present, and exit with code 0 when the issue is fixed.