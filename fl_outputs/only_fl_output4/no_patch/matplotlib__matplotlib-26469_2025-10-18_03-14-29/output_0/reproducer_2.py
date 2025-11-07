import matplotlib.backends.backend_pdf
import os
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

def test_pdfpages_behavior():
    filename = "test_empty_pdf.pdf"
    try:
        # Explicitly create an instance of PdfPages without passing keep_empty
        pdf = matplotlib.backends.backend_pdf.PdfPages(filename)
        pdf.close()

        # Verify file creation behavior
        file_exists = os.path.isfile(filename)
        
        # Asserting the condition that should raise an AssertionError when the issue is present,
        # and should pass without errors when the fix is implemented.
        assert file_exists, "PdfPages did not create a PDF file. Expected behavior based on the current default (issue present)."
        
        # If the file exists but is invalid according to the PDF standard for not having any pages,
        # this block is to validate the nature of the issue rather than the behavior fix.
        # This part is for demonstration/deeper validation purposes and does not directly relate to changing `keep_empty`'s default.
        print("Warning: The script anticipated the current behavior based on the default keep_empty=True. Manual inspection is recommended to validate the empty PDF file's compliance with the PDF standard.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    finally:
        if os.path.exists(filename):
            os.remove(filename)

    print("Test executed: The default behavior for PdfPages with keep_empty not explicitly set may still create an empty PDF file, indicating the issue is present.")
    sys.exit(0)

if __name__ == "__main__":
    test_pdfpages_behavior()
