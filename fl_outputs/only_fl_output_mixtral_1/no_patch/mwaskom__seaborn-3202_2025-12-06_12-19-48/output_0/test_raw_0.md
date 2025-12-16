 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import seaborn as sns
import seaborn.objects as so
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

penguins = sns.load_dataset("penguins")

try:
    so.Plot(penguins.dropna(), x="sex", y="bill_depth_mm") \
        .add(so.Dots()) \
        .facet(col="species", row="island")
except Exception as e:
    print_stacktrace(e)
    assert False
```
When executed with `python3 reproducer.py`, the script will print the stack trace of the issue.

The expected behavior is similar to `catplot`, where the facets that contain no data are empty. The following code demonstrates this behavior:
```python
sns.catplot(data=penguins.dropna(), x="sex", y="bill_depth_mm", col="species", row="island")
```
![example](https://user-images.githubusercontent.com/13831112/207851197-92830add-4aa4-49a5-a341-c71ac76eb1d2.png)