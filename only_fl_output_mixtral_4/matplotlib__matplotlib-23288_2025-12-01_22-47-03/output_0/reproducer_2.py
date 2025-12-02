import matplotlib.pyplot as plt
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

def reproduce():
    plt.text(0.5, 0.5, "Long text with link", rotation=45, url="https://matplotlib.org")
    plt.savefig("link.pdf")

if __name__ == "__main__":
    try:
        reproduce()
        assert False, "The URL-sensitive area should be rotated in the PDF output"
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
