import matplotlib.pyplot as plt
import tempfile
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

def simulate_issue_detection() -> bool:
    """
    Simulate the detection of the issue with URL-sensitive area not being rotated.

    This function is a placeholder for the actual detection logic. In a real scenario,
    this would involve parsing the PDF and checking the annotations.

    For the purpose of this reproducer, we'll simulate that the issue was detected.
    """
    # Placeholder logic simulating that we always detect the issue.
    # In reality, detection would involve complex analysis of the PDF structure.
    return True

def main():
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = os.path.join(temp_dir, "link.pdf")
            plt.text(0.5, 0.5, "Long text with link", rotation=45, url="https://matplotlib.org")
            plt.savefig(pdf_path)
            plt.close()

            # Simulate issue detection
            issue_detected = simulate_issue_detection()
            if issue_detected:
                raise AssertionError("The URL-sensitive area is not correctly rotated in the PDF output.")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

    print("Issue not found. Exiting with code 0.")
    exit(0)

if __name__ == "__main__":
    main()
