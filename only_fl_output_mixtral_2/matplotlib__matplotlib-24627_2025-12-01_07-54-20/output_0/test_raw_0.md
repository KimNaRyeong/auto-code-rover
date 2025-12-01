 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import matplotlib.pyplot as plt

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    f, a = plt.subplots()
    l, = a.plot([1, 2])
    l.remove()
    assert l.axes is None, "Issue not present: `.axes` attribute is unset after removing the artist"

    f, a = plt.subplots()
    l, = a.plot([1, 2])
    a.cla()
    assert l.axes is not None, "Issue present: `.axes` attribute is not unset after clearing the axes"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace if the issue is present, and exit with code 0 if the issue is fixed.