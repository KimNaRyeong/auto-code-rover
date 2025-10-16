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

def main():
    import subprocess
    import sys

    command = [sys.executable, "-m", "pylint", "-Q"]
    
    try:
        completed_process = subprocess.run(command, text=True, capture_output=True, check=True)
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        error_output = e.stderr
        if "unrecognized-option" in error_output and "_UnrecognizedOptionError" in error_output:
            print("Issue reproduced successfully.", file=sys.stdout)
            sys.exit(0)  # Exit with 0 to indicate successful reproduction
        else:
            raise AssertionError("The expected issue was not reproduced correctly.") from e

    raise AssertionError("The issue should have triggered an error, but it did not.")

if __name__ == "__main__":
    main()
