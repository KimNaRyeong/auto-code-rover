import subprocess
import re
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def run_make(makefile, target):
    try:
        subprocess.check_call(["make", "-f", makefile, target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        assert False

def check_pdf_output(pdf_file):
    with open(pdf_file, "r") as f:
        content = f.read()
    pattern = r"A first footnote\nA second footnote\nFirst reference to first footnote \?\nFirst reference to second footnote \[\d+\]\nSecond reference to first footnote \?\nSecond reference to second footnote \[\d+\]"
    if re.search(pattern, content):
        print("PDF output contains '?' instead of footnote numbers.")
        print_stacktrace(Exception("PDF output contains '?' instead of footnote numbers."))
        assert False

if __name__ == "__main__":
    makefile = "Makefile"
    target = "latexpdf"
    pdf_file = "build/latex/index.pdf"
    run_make(makefile, target)
    check_pdf_output(pdf_file)
    print("No issues found in the PDF output.")
