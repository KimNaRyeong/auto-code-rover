Here is the reproducer script:

```python
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO
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
    sns.set()
    data = sns.load_dataset('iris')
    g = sns.relplot(data=data, x='sepal_length', y='petal_width', col='species', 
                    col_wrap=2, height=2.5)
    g.set_titles(row_template="{row_name}", col_template="SOMEWHATLONG-{col_name}")
    for axes in g.axes.flat:
        axes.ticklabel_format(axis='both', style='scientific', scilimits=(0, 0))

    buf = StringIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img = buf.getvalue()

except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```

This script will attempt to reproduce the issue by creating a seaborn relplot with overlapping labels. If the issue is present, it will raise an `AssertionError` and print the stack trace.