import subprocess
import sys
import os

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

def main():
    try:
        # Ensure psql is installed and available
        if not os.path.exists('/usr/bin/psql'):
            raise AssertionError("psql is not installed")

        # Reproduce the issue
        command = ["psql", "--", "-c", "select * from some_table;", "some_database"]
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        if b"warning: extra command-line argument" not in output:
            raise AssertionError("Issue is not present")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
