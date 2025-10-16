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

def test_memoryview_response():
    # Minimal Django environment setup
    from django.conf import settings
    settings.configure()
    from django.http import HttpResponse

    # Simulate the issue
    try:
        memory_view_content = memoryview(b"My Content")
        response = HttpResponse(memory_view_content)
        actual_content = response.getvalue()  # Using getvalue to extract the buffer content

        # Check if the issue is reproduced
        assert actual_content == b"My Content", "HttpResponse does not handle memoryview objects correctly."

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error code to signal failure

if __name__ == "__main__":
    test_memoryview_response()
    print("Issue not present or resolved.")
    sys.exit(0)  # Exit with success code
