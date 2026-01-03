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

def test_xoptions():
    args = [sys.executable, "-X", "utf8", "manage.py", "runserver", "0.0.0.0:8005", "-v3", "--noreload"]
    try:
        subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        assert False, "The script should not have returned a non-zero exit status."

if __name__ == "__main__":
    test_xoptions()
