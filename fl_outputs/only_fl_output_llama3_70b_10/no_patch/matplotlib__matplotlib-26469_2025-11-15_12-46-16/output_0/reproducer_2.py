import matplotlib.backends.backend_cairo as cairo
from matplotlib.backends.backend_pdf import PdfPages
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

def test_keep_empty():
    pdf_file = "/tmp/test.pdf"
    if os.path.exists(pdf_file):
        os.remove(pdf_file)

    with PdfPages(pdf_file, keep_empty=True) as pages:
        pass  # No figures added

    assert os.path.exists(pdf_file), "Pdf file was not created with zero pages"

try:
    test_keep_empty()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
