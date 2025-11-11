import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        setting = {1: {'login': 'cooper', 'password': 'secret'}}
        from django.conf import settings
        settings.SOME_SETTING = setting
        settings.cleanse_setting(setting)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected exception not raised")

if __name__ == "__main__":
    main()
