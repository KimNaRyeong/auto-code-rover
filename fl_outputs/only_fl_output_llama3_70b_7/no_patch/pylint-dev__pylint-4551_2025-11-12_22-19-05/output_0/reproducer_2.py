import os
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

# Check if pyreverse is installed
try:
    subprocess.check_output(["pyreverse", "--version"])
except FileNotFoundError:
    raise AssertionError("Pyreverse is not installed")

# Create a Python file with the class definition
with open("example.py", "w") as f:
    f.write("""
class C(object):
    def __init__(self, a: str = None):
        self.a = a
""")

try:
    # Generate UML diagram using pyreverse
    subprocess.check_output(["pyreverse", "-o", "classes_test", "-ASmy", "example"])

    # Check if type hint is present in the output
    with open("classes_test.dot", "r") as f:
        content = f.read()
        assert "a : String" in content, "Type hint not found in UML diagram"

except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

os.remove("example.py")
os.remove("classes_test.dot")

sys.exit(0)
