import os
from matplotlib.backends.backend_pgf import PdfPages

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

def test_keep_empty_default():
    pdf_file = "/tmp/foo.pdf"
    try:
        with PdfPages(pdf_file) as pdf:
            pass  # no figures added
        assert os.path.exists(pdf_file), "Expected PDF file to exist"
        pdf_size = os.path.getsize(pdf_file)
        assert pdf_size > 0, f"Expected non-empty PDF file, but got {pdf_size} bytes"
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    test_keep_empty_default()
    exit(0)
