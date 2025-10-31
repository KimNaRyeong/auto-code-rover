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

def main():
    try:
        sns.set()
        sns.set_style("white")

        data = (sns.load_dataset('iris').set_index('species')*1e7).reset_index()
        g = sns.relplot(data=data, x='sepal_length', y='sepal_width', col='species', 
                        col_wrap=2, height=2.5, facet_kws=dict(sharex=False, sharey=False))
        g.set_titles(row_template="{row_name}", col_template="SOMEWHATLONG-{col_name}")
        for axes in g.axes.flat:
            axes.ticklabel_format(axis='both', style='scientific', scilimits=(0, 0))

        buf = StringIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img = buf.getvalue()

        if "Overlapping" not in img:
            raise AssertionError("Issue fixed")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

This script will execute the code that reproduces the issue and check if the image contains the string "Overlapping". If it does not, an `AssertionError` is raised. The stack trace of the error is then printed to the console and the script exits with a non-zero status code.