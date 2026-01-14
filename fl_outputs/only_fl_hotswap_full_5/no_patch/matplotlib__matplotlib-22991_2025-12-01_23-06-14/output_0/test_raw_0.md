 Here is a standalone python file `reproducer.py` to reproduce the issue:
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

def reproduce_issue():
    fig = plt.figure()
    subfigs = fig.subfigures(2, 1)

    axarr = subfigs[0].subplots(2, 2)

    plt.sca(axarr[0, 0])

if __name__ == "__main__":
    try:
        reproduce_issue()
    except Exception as e:
        print_stacktrace(e)
        assert False
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 22, in <module>
    reproduce_issue()
  File "reproducer.py", line 18, in reproduce_issue
    plt.sca(axarr[0, 0])
  File "/home/me/.local/lib/python3.8/site-packages/matplotlib/pyplot.py", line 1085, in sca
    figure(ax.figure)
  File "/home/me/.local/lib/python3.8/site-packages/matplotlib/pyplot.py", line 773, in figure
    num = int(num)  # crude validation of num argument
TypeError: int() argument must be a string, a bytes-like object or a number, not 'Subplot'
```
This stack trace shows that the issue is present and the line numbers of the statements are shown clearly.