import matplotlib.backends.backend_pdf as pdf
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
    pp = pdf.PdfPages("/tmp/foo.pdf")
    pp.close()
    assert os.path.exists("/tmp/foo.pdf"), "PdfPages with zero figures should be written to disk"
    try:
        with open("/tmp/foo.pdf", 'rb') as f:
            pdf_data = f.read()
        assert len(pdf_data) > 0, "PdfPages with zero figures should not produce an empty file"
    except Exception as e:
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == "__main__":
    try:
        test_keep_empty()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
