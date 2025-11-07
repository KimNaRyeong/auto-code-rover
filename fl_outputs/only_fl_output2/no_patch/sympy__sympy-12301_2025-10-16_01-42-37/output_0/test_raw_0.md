```python
# reproducer.py
import sympy
import os

def run_test():
    try:
        os.environ['PYTHONHASHSEED'] = '736538842'
        result = sympy.test(split='4/4', seed=57601301)
        if result.failed:
            raise AssertionError("Test failed.")
    except Exception as e:
        print_stacktrace(e)
        raise

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
    run_test()
```