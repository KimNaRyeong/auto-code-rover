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

try:
    result = subprocess.run([sys.executable, '-m', 'pylint', 'mytest.py', '-v'], 
                            capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as e:
    print_stacktrace(e)
    assert "argument --verbose/-v: expected one argument" in str(e), "Issue not reproduced"
else:
    print("Issue fixed")
    sys.exit(0)

sys.exit(1)
