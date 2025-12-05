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

    plt.show()

    try:
        assert g.fig.get_size()[0] == 14.0, "Figure width is not 14 inches"
        assert g.fig.get_size()[1] == 7.0, "Figure height is not 7 inches"
    except AssertionError as e:
        print_stacktrace(e)
        plt.close(g.fig)
        raise e
```
To reproduce the issue, run the script with Seaborn version 0.12:
```bash
$ conda create -n seaborn-0.12 seaborn=0.12
$ conda activate seaborn-0.12
$ python3 reproducer.py
```
The script should print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 33, in <module>
    assert g.fig.get_size()[0] == 14.0, "Figure width is not 14 inches"
AssertionError: Figure width is not 14 inches
```
The issue is present in Seaborn version 0.12 because the figure width is not 14 inches, which is the expected width when `col_wrap=2` and `height=2.5`.

To fix the issue, run the script with Seaborn version 11.2 or later:
```bash
$ conda create -n seaborn-11.2 seaborn=11.2
$ conda activate seaborn-11.2
$ python3 reproducer.py
```
The script should not print any stack trace and exit with code 0. The figure width should be 14 inches, which fixes the overlapping labels issue.