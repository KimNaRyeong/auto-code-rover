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
    pdf_file = "/tmp/foo.pdf"
    with PdfPages(pdf_file, keep_empty=True) as pdf:
        pass  # no figures added
    assert os.path.exists(pdf_file), "Pdf file was not created"
    try:
        cairo.PdfSurface(pdf_file)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Pdf file is invalid")

try:
    test_keep_empty()
except AssertionError as e:
    print_stacktrace(e)
    raise
else:
    print("Issue is present, PdfPages created an empty PDF file")
