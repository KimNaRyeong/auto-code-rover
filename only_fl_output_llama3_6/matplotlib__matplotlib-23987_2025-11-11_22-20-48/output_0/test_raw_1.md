Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import matplotlib.pyplot as plt
import numpy as np
from functools import wraps

def assert_raises(expected_exception, func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except expected_exception:
            print_stacktrace()
            raise AssertionError("Expected exception not raised")
        else:
            exit(0)

    return wrapper

@assert_raises(UserWarning, plt.subplots_adjust)
def reproduce_issue():
    import matplotlib.pyplot as plt
    import numpy as np
    a = np.linspace(0,2*np.pi,100)
    b = np.sin(a)
    c = np.cos(a)
    fig,ax = plt.subplots(1,2,figsize=(8,2),constrained_layout=False)
    ax[0].plot(a,b)
    ax[1].plot(a,c)
    plt.subplots_adjust(wspace=0)

reproduce_issue()
```

This script uses the `assert_raises` decorator to catch any `UserWarning` exceptions raised by the `plt.subplots_adjust` function. If a warning is raised, it prints the stack trace using the `print_stacktrace` function and raises an `AssertionError`. If no warning is raised, it exits with code 0.

To run this script, save it as `reproducer.py` in the root directory of your project and execute it with `python3 reproducer.py`.