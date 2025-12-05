 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from django.contrib.messages.storage.base import Message
from django.contrib.messages.storage.cookie import MessageEncoder, MessageDecoder

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    original_message = Message(10, "Here is a message", extra_tags="")
    encoded_message = MessageEncoder().encode(original_message)
    decoded_message = MessageDecoder().decode(encoded_message)
    assert original_message.extra_tags == "", "extra_tags should be an empty string"
    assert decoded_message.extra_tags is not None, "extra_tags should not be None"
    assert original_message.extra_tags == decoded_message.extra_tags, "extra_tags should be the same"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print a stack trace, demonstrating the issue. The script should exit with code 1.

To fix the issue, you can modify the `MessageEncoder` class to check for `extra_tags is not None` instead of checking for truthyness. Here is an example of how you can modify the `MessageEncoder` class:
```python
class FixedMessageEncoder(MessageEncoder):
    def encode(self, message):
        if message.extra_tags is not None:
            data['extra_tags'] = message.extra_tags
        return super().encode(message)
```
You can then replace the `MessageEncoder()` calls in the `reproducer.py` script with `FixedMessageEncoder()` to demonstrate that the issue has been fixed.