Here is the reproducer script:

```python
import seaborn as sns
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

        if len(img) < 10000:  # Check the size of the image
            raise AssertionError("Image is too small")
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```

This script will run the code that reproduces the issue and check if the generated image is larger than a certain threshold. If it's not, an `AssertionError` will be raised with a stack trace printed to the console.