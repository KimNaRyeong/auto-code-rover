import sys
from argparse import ArgumentParser, SUPPRESS

def main():
    parser = ArgumentParser(description='Pylint Reproducer')
    parser.add_argument('-v', '--verbose')

    try:
        args = parser.parse_args()
        if not args.verbose:
            raise AssertionError("Argument expected for short verbose option")

    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    print("Issue reproduced successfully")

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

if __name__ == "__main__":
    main()
