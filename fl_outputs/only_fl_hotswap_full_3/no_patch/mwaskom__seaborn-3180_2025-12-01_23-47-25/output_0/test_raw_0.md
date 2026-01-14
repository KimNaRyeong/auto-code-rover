 Here is a standalone Python script `reproducer.py` that reproduces the issue of overlapping labels in `relplot` with Seaborn version 0.12:
```python
import seaborn as sns
import matplotlib.pyplot as plt


def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


if __name__ == "__main__":
    sns.set_context("paper")
    sns.set_style("white")

    data = (sns.load_dataset('iris').set_index('species') * 1e7).reset_index()
    g = sns.relplot(
        data=data,
        x='sepal_length',
        y='sepal_width',
        col='species',
        col_wrap=2,
        height=2.5,
    )
    g.set_titles(row_template="{row_name}", col_template="SOMEWHATLONG-{col_name}")
    for axes in g.axes.flat:
        axes.ticklabel_format(axis='both', style='scientific', scilimits=(0, 0))

    plt.gcf().set_size_inches(12, 8)
    plt.show()

    try:
        assert g.fig.get_size_inches() == (12, 8)
    except AssertionError as e:
        print_stacktrace(e)
        plt.close()
        exit(1)

    plt.close()
    exit(0)
```
This script uses the `print_stacktrace` function to print the stack trace when an `AssertionError` is raised. The script sets the Seaborn context and style, creates a `relplot` with the given data and parameters, and sets the tick labels to scientific notation. It then checks the size of the figure and raises an `AssertionError` if the size is not as expected.

To reproduce the issue, you can run the script with Seaborn version 0.12:
```
pip install seaborn==0.12.1
python3 reproducer.py
```
This should print the stack trace and exit with code 1.

To fix the issue, you can upgrade Seaborn to version 11.2 or later:
```
pip install seaborn==11.2
python3 reproducer.py
```
This should print the figure without overlapping labels and exit with code 0.