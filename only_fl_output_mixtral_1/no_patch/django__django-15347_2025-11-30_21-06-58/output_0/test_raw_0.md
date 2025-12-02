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
        print("Issue is fixed.")
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print a stack trace of the issue. The stack trace should show that the `extra_tags` attribute of the `decoded_message` object is `None`, while the `extra_tags` attribute of the `original_message` object is an empty string. This demonstrates the issue where the messages framework incorrectly serializes/deserializes extra\_tags when it's an empty string.