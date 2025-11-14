It seems that the issue is not with the `randomized_svd` function itself, but rather with the installation of scikit-learn. The error message suggests that scikit-learn has not been built correctly.

To reproduce this issue, you can create a standalone Python file `reproducer.py` as follows:

```python
import sys

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

def main():
    try:
        from sklearn.utils.extmath import randomized_svd
    except ImportError as e:
        raise AssertionError("Issue present") from e
    else:
        print("Issue fixed")

if __name__ == "__main__":
    main()
```

This script will attempt to import the `randomized_svd` function from scikit-learn. If the import fails due to an installation issue, it will raise an `AssertionError` and print a stack trace.

To run this script, execute the following command:

```
python3 reproducer.py
```

If the issue is present, you should see an error message indicating that the module was not found.