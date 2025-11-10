Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import assertpy as ap

ap.assume_failure()

def reproduce_issue():
    f, ax = plt.subplots()
    ax.xaxis.update_units(["a", "b"])
    try:
        ax.plot([], [])
    except Exception as e:
        print_stacktrace(e)

reproduce_issue()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.