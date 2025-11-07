import django
from django.conf import settings

# Configure Django settings to ensure the script can run standalone
settings.configure(
    SECRET_KEY="a-very-secret-key",
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.messages",
    ]
)
django.setup()

from django.contrib.messages.storage.base import Message
from django.contrib.messages.storage.cookie import MessageEncoder, MessageDecoder

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

def test_message_serialization_bug():
    try:
        # Create an original message with extra_tags as an empty string
        original_message = Message(10, "Here is a message", extra_tags="")
        # Serialize the message
        encoded_message = MessageEncoder().encode(original_message)
        # Deserialize the message
        decoded_message = MessageDecoder().decode(encoded_message)

        # Checking if the deserialized message's extra_tags is None instead of an empty string
        assert original_message.extra_tags == "", "Original message extra_tags should be an empty string."
        assert decoded_message.extra_tags is not None, "Decoded message extra_tags should not be None."
    except AssertionError as e:
        print_stacktrace(e)
        # Exit with an error signifying the bug is present
        exit(1)
    else:
        print("The test passed successfully, no issues found.")

if __name__ == '__main__':
    test_message_serialization_bug()
    # Exit with code 0 when the issue is fixed or not present
    exit(0)
