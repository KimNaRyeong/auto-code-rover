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

def main():
    class FITSFile:
        def __init__(self, filename):
            self.filename = filename

        def compare(self, other):
            if self.filename == other.filename:
                return True
            return False

    file1 = FITSFile('diffbug.fits')
    file2 = FITSFile('diffbug.fits')

    try:
        assert file1.compare(file2)
    except AssertionError:
        pass
    else:
        print_stacktrace(AssertionError("`FITSFile` did not report differences between identical files."))
        sys.exit(1)

    print(file1.compare(file2))

if __name__ == "__main__":
    main()
