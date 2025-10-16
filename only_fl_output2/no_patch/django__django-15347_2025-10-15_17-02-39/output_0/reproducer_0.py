# reproducer.py
def main():
    try:
        # Setting up the minimal Django environment for messages to work
        from django.conf import settings
        settings.configure(USE_I18N=False, USE_L10N=False, USE_TZ=False,
                           DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
                           INSTALLED_APPS=('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.messages',),
                           SECRET_KEY='dummy')

        # Import necessary components for message encoding/decoding
        from django.contrib.messages.storage.base import Message
        from django.contrib.messages.storage.cookie import MessageEncoder, MessageDecoder
        import django
        django.setup()

        # Creating a message with extra_tags as an empty string
        original_message = Message(10, "Here is a message", extra_tags="")
        # Encoding the message
        encoded_message = MessageEncoder().encode(original_message)
        # Decoding the encoded message
        decoded_message = MessageDecoder().decode(encoded_message)

        # Assertion to check if the bug exists
        assert original_message.extra_tags == "", "The original_message.extra_tags should be an empty string."
        assert decoded_message.extra_tags == "", f"Decoded extra_tags should be an empty string, found: {decoded_message.extra_tags}"

    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from e
    else:
        print("No issue found. The extra_tags field is correctly serialized and deserialized as an empty string.")

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

if __name__ == "__main__":
    main()
