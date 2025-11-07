```python
# reproducer.py
import sys

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
    from django.conf import settings
    settings.configure()

    from django.contrib.messages.storage.base import Message
    from django.contrib.messages.storage.cookie import MessageEncoder, MessageDecoder

    original_message = Message(10, "Here is a message", extra_tags="")
    encoded_message = MessageEncoder().encode(original_message)
    decoded_message = MessageDecoder().decode(encoded_message)

    try:
        assert original_message.extra_tags == "", "Original message extra_tags should be an empty string."
        assert decoded_message.extra_tags == "", "Decoded message extra_tags should not turn into None."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error code to show failure in reproducing the issue correctly.

    print("The issue has been fixed. Exiting with code 0.")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

This script will reproduce the issue mentioned concerning the Django Messages framework. When executed, it attempts to serialize and then deserialize a message object with `extra_tags` as an empty string. According to the issue, `extra_tags` should remain an empty string, but gets converted to `None` instead due to the improper serialization/deserialization logic. The `assert` statements are used to ensure that `extra_tags` remains an empty string after being decoded, raising an `AssertionError` if this is not the case, which triggers the `print_stacktrace` function to display the error details. The script exits with code 0 if there no errors, indicating the issue is fixed.