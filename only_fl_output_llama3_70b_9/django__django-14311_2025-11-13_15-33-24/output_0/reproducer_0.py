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
        output, _ = process.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        raise AssertionError("Autoreload did not work as expected")

    # Check if the command was executed correctly
    assert b'runserver' in output, "Runserver function was not called"

if __name__ == '__main__':
    try:
        test_autoreload()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
