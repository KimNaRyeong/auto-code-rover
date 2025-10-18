# reproducer.py

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

def main():
    # To ensure this script is standalone, configure settings on the fly
    from django.conf import settings
    settings.configure(
        SECRET_KEY='a-very-secret-key',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.messages',
        ]
    )

    # Django setup is required to populate the app registry & avoid ImproperlyConfigured exceptions
    import django
    django.setup()
    
    # Now import the messages components
    from django.contrib.messages.storage.base import Message
    from django.contrib.messages.storage.cookie import MessageEncoder, MessageDecoder
    
    # Case setup
    original_message = Message(10, "Here is a message", extra_tags="")
    encoded_message = MessageEncoder().encode(original_message)
    decoded_message = MessageDecoder().decode(encoded_message)
    
    # Assert to raise an error if the bug is present
    try:
        # Expected behavior: extra_tags="" remains the same after encoding and decoding
        assert original_message.extra_tags == "", "Original extra_tags should be an empty string"
        assert decoded_message.extra_tags == "", "Decoded extra_tags was incorrectly set to None instead of an empty string"
        print("No issue detected, `extra_tags` preserved correctly.")
    except AssertionError as e:
        print_stacktrace(e)
        raise  # Re-raise the assertion to make the script exit with an error

if __name__ == "__main__":
    main()
