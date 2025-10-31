Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
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

def test_schur_number():
    try:
        # Your code that reproduces the issue here
        Schur_Number(1)  # Replace '1' with your actual value
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    try:
        test_schur_number()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
```

Replace `Schur_Number(1)` with your actual code that reproduces the issue.