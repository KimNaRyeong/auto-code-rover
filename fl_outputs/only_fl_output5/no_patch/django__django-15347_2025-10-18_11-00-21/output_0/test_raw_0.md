```python
# reproducer.py
import django
from django.conf import settings

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

def setup_django_environment():
    settings.configure(
        SECRET_KEY='a-very-secret-key',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.messages',
        ]
    )
    django.setup()

def test_message_serialization_bug():
    from django.contrib.messages.storage.base import Message
    from django.contrib.messages.storage.cookie import MessageEncoder, MessageDecoder

    original_message = Message(10, "Here is a message", extra_tags="")
    encoded_message = MessageEncoder().encode(original_message)
    decoded_message = MessageDecoder().decode(encoded_message)

    # Check if the issue is present
    assert original_message.extra_tags == "", "Original extra_tags should be an empty string."
    try:
        assert decoded_message.extra_tags == "", "Deserialized extra_tags should be an empty string, not None."
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    setup_django_environment()
    try:
        test_message_serialization_bug()
    except AssertionError:
        print("Issue reproduced.")
        exit(1) # Exit with a non-zero code to indicate failure
    print("Issue not present.")
    exit(0)
```