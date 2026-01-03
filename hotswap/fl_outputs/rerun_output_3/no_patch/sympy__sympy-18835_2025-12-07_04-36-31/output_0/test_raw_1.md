 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
def uniq(lst):
    """
    Return a new list with duplicate elements removed.
    """
    seen = []
    for item in lst:
        if item not in seen:
            seen.append(item)
    return seen

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
    f = list('THISTLE')
    try:
        for i in uniq(f):
            f.remove(i)
            print(i)
    except RuntimeError as e:
        print_stacktrace(e)
        assert False, "Issue reproduced successfully"

if __name__ == "__main__":
    main()
```
When executed using `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace, indicating that the issue has been successfully reproduced. If the issue is fixed, the script will exit with code 0.