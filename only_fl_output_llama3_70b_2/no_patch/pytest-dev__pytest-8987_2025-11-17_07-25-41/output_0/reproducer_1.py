import os
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

if __name__ == "__main__":
    try:
        result = subprocess.run(['pytest', '-vk', 'test_solution[foo.py-5\\n10\\n-16\\n]', 'reproducer.py'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert result.returncode == 0
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        raise AssertionError("pytest -k doesn't work with '\\'")
    else:
        print("Issue is fixed")
