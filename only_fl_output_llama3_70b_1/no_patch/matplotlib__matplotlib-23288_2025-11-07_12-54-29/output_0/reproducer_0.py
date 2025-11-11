import matplotlib.pyplot as plt
import os

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

def test_url_area_rotation():
    plt.text(0.5, 0.5, "Long text with link", rotation=45, url="https://matplotlib.org")
    plt.savefig("link.pdf")

try:
    test_url_area_rotation()
    assert False, "URL area is not rotated in PDF output"
except AssertionError as e:
    print_stacktrace(e)
    os._exit(1)  # Exit with code 1 to indicate the issue is present
