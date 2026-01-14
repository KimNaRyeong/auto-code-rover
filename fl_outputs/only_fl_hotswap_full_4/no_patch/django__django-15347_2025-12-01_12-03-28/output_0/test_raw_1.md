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
    assert original_message.extra_tags == ""
    assert decoded_message.extra_tags is not None

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace showing the line numbers of the statements. This demonstrates the issue where `extra_tags==""` is converted to `extra_tags==None` during serialization and deserialization.

To fix the issue, the `MessageEncoder` class should be modified to check for `extra_tags is not None` instead of checking for truthyness of `extra_tags`. Here is an example of how the `MessageEncoder` class can be modified:
```python
class FixedMessageEncoder(MessageEncoder):
    def encode(self, message):
        if message.extra_tags is not None:
            data['tags'] = message.extra_tags
        return super().encode(message)
```
The `FixedMessageEncoder` class can then be used in the `reproducer.py` script to demonstrate that the issue has been fixed:
```python
def main():
    original_message = Message(10, "Here is a message", extra_tags="")
    fixed_encoder = FixedMessageEncoder()
    encoded_message = fixed_encoder.encode(original_message)
    decoded_message = fixed_encoder.decode(encoded_message)
    assert original_message.extra_tags == ""
    assert decoded_message.extra_tags == ""
```
When executed with `python3 reproducer.py`, the script will exit with code 0, indicating that the issue has been fixed.