Here is the reproducer script:

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

def reproduce_issue():
    fixture_dirs = [Path('dir1'), Path('dir2'), Path('dir3')]
    try:
        from django.core.management import loaddata
        loaddata(fixture_dirs)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue reproduced successfully.")
        exit(0)
```

This script attempts to load fixture directories using the `loaddata` function from Django's management commands. If an exception is raised during this process, it prints the stack trace and raises the same exception.