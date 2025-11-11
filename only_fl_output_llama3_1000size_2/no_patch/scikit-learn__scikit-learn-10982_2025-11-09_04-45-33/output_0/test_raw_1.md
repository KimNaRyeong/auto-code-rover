It seems that the issue is not with the RandomizedSearchCV class itself, but rather with the installation of scikit-learn. The error message suggests that scikit-learn has not been built correctly.

To reproduce this issue, you would need to install scikit-learn from source and then run a script that attempts to import it. Here is an example reproducer script:

```
import sys
from sklearn.model_selection import RandomizedSearchCV

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
    try:
        from sklearn.model_selection import RandomizedSearchCV
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script attempts to import the RandomizedSearchCV class, which should raise an ImportError if scikit-learn is not installed correctly.