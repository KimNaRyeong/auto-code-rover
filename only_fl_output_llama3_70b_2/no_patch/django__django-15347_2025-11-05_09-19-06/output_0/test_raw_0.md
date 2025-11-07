Here is the `reproducer.py` file to reproduce the issue:
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
This script sets up a Django environment, creates an original message with `extra_tags` set to an empty string, encodes and decodes the message using the `MessageEncoder` and `MessageDecoder`, and then asserts that the `extra_tags` attribute of both messages is still an empty string. If the assertion fails (i.e., if the issue is present), it prints a stack trace of the error and exits with code 1. If the issue is fixed, the script exits with code 0.