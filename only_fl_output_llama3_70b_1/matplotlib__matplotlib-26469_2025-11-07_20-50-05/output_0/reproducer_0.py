import matplotlib.backends.backend_pdf
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
    pdf = matplotlib.backends.backend_pdf.PdfPages("test.pdf", keep_empty=True)
    pdf.close()

    assert os.path.exists("test.pdf"), "PDF file was not created"
    try:
        with open("test.pdf", 'rb') as f:
            pdf_data = f.read()
        assert len(pdf_data) > 0, "PDF file is empty"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Invalid PDF file created")

if __name__ == "__main__":
    test_keep_empty()
