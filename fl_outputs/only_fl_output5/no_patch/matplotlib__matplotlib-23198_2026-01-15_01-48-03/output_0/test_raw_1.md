Given the instructions, here is a Python script designed to highlight the inconsistency between the `ncol`/`ncols` and `nrow`/`nrows` parameters in Matplotlib's API. This script will attempt to use `ncol` with `plt.subplots` and `ncols` with `axis.legend()` to demonstrate the inconsistency, aiming to fail and showcase it via assertion errors. The approach is slightly artificial as it's designed to illustrate the issue rather than check for conventionally correct usage, which does not exist as described. However, it satisfies the request to raise an error reflecting the described problem.

```python
import matplotlib.pyplot as plt

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
    # Intentionally using the 'wrong' kwargs to demonstrate the inconsistency.
    # These calls are expected to fail if the inconsistency issue is present.
    try:
        fig, axs = plt.subplots(ncol=2)
        raise AssertionError("plt.subplots unexpectedly accepted 'ncol'. The inconsistency issue may have been resolved.")
    except TypeError:
        # Expected failure, moving on to the next test
        pass
    
    try:
        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1], label='test')
        ax.legend(ncols=2)
        raise AssertionError("ax.legend unexpectedly accepted 'ncols'. The inconsistency issue may have been resolved.")
    except TypeError as e:
        # This is expected to fail due to the inconsistency.
        print_stacktrace(e)
        raise AssertionError("The inconsistency issue is present: ax.legend does not accept 'ncols', only 'ncol'.")

if __name__ == "__main__":
    main()
```

This script will fail in its current form, as it deliberately misuses the API to highlight the inconsistency mentioned. It tries to use `ncol` with `plt.subplots()` — which is expected to fail (because the correct kwarg is `ncols`) — and then attempts to use `ncols` with `ax.legend()`, aiming to fail due to the correct argument being `ncol`. The intent is to cause a contradiction and thus provoke an error, illustrating the inconsistency. When executed, it should demonstrate the flaw directly if and only if the inconsistency exists as described; otherwise, it may indicate that the inconsistency has been addressed or does not exist as anticipated.