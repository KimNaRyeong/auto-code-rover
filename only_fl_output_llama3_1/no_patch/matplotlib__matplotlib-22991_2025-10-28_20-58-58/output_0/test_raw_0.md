Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import traceback
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

try:
    import matplotlib.pyplot as plt

    fig = plt.figure()
    subfigs = fig.subfigures(2, 1)

    axarr = subfigs[0].subplots(2, 2)

    plt.sca(axarr[0, 0])
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue should not be present")
finally:
    if hasattr(globals(), 'plt'):
        import matplotlib.pyplot as plt
        plt.close('all')
```

This script will attempt to reproduce the issue by creating a figure with subfigures and then trying to set one of the axes as the current axis using `plt.sca()`. If an exception is raised, it will print the stack trace and raise an `AssertionError` indicating that the issue should not be present.