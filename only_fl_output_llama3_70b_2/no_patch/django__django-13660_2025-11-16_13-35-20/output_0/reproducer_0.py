import subprocess
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
    command = """
import django
def f():
    print(django.__version__)
f()
"""
    try:
        subprocess.check_output(['python', '-m', 'django', 'shell', '-c'], input=command.encode())
    except subprocess.CalledProcessError as e:
        if e.returncode != 0:
            raise AssertionError("Issue is present") from e
    else:
        print("Issue is fixed")

if __name__ == "__main__":
    main()
