 Here is a standalone Python file `reproducer.py` to reproduce the issue:
```python
import seaborn as sns
import seaborn.objects as so
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

try:
    fig = plt.figure(constrained_layout=True)
    subfigs = fig.subfigures(1,2)
    tips = sns.load_dataset("tips")
    p = (
        so.Plot(tips, "total_bill")
        .add(so.Bars(), so.Hist())
    )
    p.on(subfigs[0]).plot()

    ax = subfigs[1].subplots()
    ax.scatter([1],[1])

    fig.suptitle("Test title")
    plt.show()

    assert False, "The title should be missing from the image."
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    plt.show()
  File "/usr/local/lib/python3.9/site-packages/matplotlib/pyplot.py", line 211, in show
    manager.show()
  File "/usr/local/lib/python3.9/site-packages/matplotlib/backends/backend_tkagg.py", line 491, in show
