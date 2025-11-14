# reproducer.py

import os
import sys
import subprocess

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

def test_autoreload():
    # Create a sample module with a dotted name
    os.makedirs('foo/bar', exist_ok=True)
    with open('foo/bar/baz.py', 'w') as f:
        f.write("def runserver(): pass\n")

    # Run the command that should autoreload
    cmd = [sys.executable, '-m', 'foo.bar.baz', 'runserver']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        process.wait(timeout=5)  # Wait for 5 seconds to allow the autoreloader to kick in
    except subprocess.TimeoutExpired:
        pass

    # Check if the command is still running (i.e., autoreload worked)
    if process.poll() is None:
        print("Autoreload successful!")
        sys.exit(0)  # Exit with code 0
    else:
        raise AssertionError("Autoreload failed!")

if __name__ == '__main__':
    try:
        test_autoreload()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with code 1 on error
