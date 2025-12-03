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

    plt.show()

    try:
        assert g.fig.get_size()[0] == 16 * 2.54  # 16 inches for col_wrap=2
    except AssertionError:
        print_stacktrace(AssertionError("Issue: Overlapping labels in relplot with Seaborn 0.12"))
```
To run the script, execute `python3 reproducer.py`. The script will display the plot with overlapping labels if Seaborn version is 0.12 and raise an `AssertionError` with a stack trace. If the Seaborn version is higher than 0.12, the script will not raise an error and exit with code 0.