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

def main():
    try:
        # Create a temporary Python file with the code that triggers the issue
        with open("temp.py", "w") as f:
            f.write('"""Docstring."""\n')
            f.write('import abc\n')
            f.write('from abc import ABC\n')
            f.write('X = ...  # type: abc.ABC\n')
            f.write('Y = ...  # type: ABC\n')

        # Run pylint on the temporary file
        cmd = "pylint --from-stdin temp.py"
        output = os.popen(cmd).read()

        # Check if the `unused-import` warning is emitted
        if "W0611: Unused import abc" not in output:
            raise AssertionError("Unused import warning should be emitted")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
