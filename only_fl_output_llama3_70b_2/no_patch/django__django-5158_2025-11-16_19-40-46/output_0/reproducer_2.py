import sys
import os

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print('  File "%s"' % frame.filename, file=sys.stderr)
        print("    %d: %s" % (line_number, code_context), file=sys.stderr)
    print("%s: %s" % (e.__class__.__name__, e), file=sys.stderr)

def main():
    try:
        os.environ.pop('DJANGO_SETTINGS_MODULE', None)  # Ensure no settings are configured
        from django.core.management import execute_from_command_line
        execute_from_command_line(['django-admin.py', 'not-a-real-command', 'test'])
    except Exception as e:
        if "Requested setting INSTALLED_APPS, but settings are not configured" in str(e):
            print_stacktrace(e)
            raise AssertionError("Expected error: Unknown command")
        else:
            print_stacktrace(e)

if __name__ == "__main__":
    main()
