Here is the reproducer script:

```python
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO
import sys
import traceback

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

def check_issue():
    try:
        sns.set()
        data = sns.load_dataset('iris')
        g = sns.relplot(data=data, x='sepal_length', y='petal_width', col='species', 
                        col_wrap=2, height=2.5)
        g.set_titles(row_template="{row_name}", col_template="SOMEWHATLONG-{col_name}")
        for axes in g.axes.flat:
            axes.ticklabel_format(axis='both', style='scientific', scilimits=(0, 0))

        plt.savefig(StringIO(), format='png')
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    check_issue()
```

This script will try to reproduce the issue by creating a seaborn plot with overlapping labels. If an exception is raised during the execution of this script, it will print the stack trace and then re-raise the exception.