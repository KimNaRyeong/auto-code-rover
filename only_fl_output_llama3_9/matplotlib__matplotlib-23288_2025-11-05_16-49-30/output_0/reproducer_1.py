import matplotlib.pyplot as plt
from io import BytesIO
import contextlib
import sys
import traceback

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

try:
    plt.text(0.5, 0.5, "Long text with link", rotation=45, url="https://matplotlib.org")
    buf = BytesIO()
    plt.savefig(buf, format='pdf')
    if not plt.show():
        raise AssertionError("URL-area not rotated in PDFs")
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
