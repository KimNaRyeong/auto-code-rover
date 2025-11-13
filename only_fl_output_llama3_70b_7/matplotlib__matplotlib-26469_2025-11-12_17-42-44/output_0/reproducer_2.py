import os
from matplotlib.backends.backend_pdf import PdfPages

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
    pdf_file = "/tmp/foo.pdf"
    try:
        with PdfPages(pdf_file) as pdf:
            pass  # create an empty PDF
    except Exception as e:
        print_stacktrace(e)
        raise
    assert os.path.exists(pdf_file), "Expected PDF file to be created"
    assert os.path.getsize(pdf_file) > 0, "Expected non-empty PDF file"

test_keep_empty()
