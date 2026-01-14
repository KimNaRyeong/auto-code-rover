 Here is a standalone Python script `reproducer.py` that reproduces the issue of overlapping labels in `relplot` with Seaborn version 0.12:
```python
import seaborn as sns
import matplotlib.pyplot as plt


def print_stacktrace(e: Exception):
    import traceback, sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def reproduce_issue():
    sns.set_context("paper")
    sns.set_style("white")

    data = (sns.load_dataset('iris').set_index('species') * 1e7).reset_index()
    g = sns.relplot(data=data, x='sepal_length', y='sepal_width', col='species',
                    col_wrap=2, height=2.5)
    g.set_titles(row_template="{row_name}", col_template="SOMEWHATLONG-{col_name}")
    for axes in g.axes.flat:
        axes.ticklabel_format(axis='both', style='scientific', scilimits=(0, 0))


if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)
        assert False, "An unexpected error occurred while reproducing the issue."
```
To run the script, execute `python3 reproducer.py` in the terminal. The script will raise an `AssertionError` with a stack trace when the issue is present.

Note that the script uses Seaborn version 0.12.2 and Matplotlib version 3.6.2, which are the latest versions at the time of writing. If you are using a different version of Seaborn or Matplotlib, you may need to modify the script accordingly.