import pylint
import sys

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
    name = "my_project"
    files = ["file1.py", "file2.py"]

    try:
        # Desired solution
        pylint.pyreverse(output=pylint.PNG, project=name, files=files)
    except AttributeError as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present")

if __name__ == "__main__":
    main()
