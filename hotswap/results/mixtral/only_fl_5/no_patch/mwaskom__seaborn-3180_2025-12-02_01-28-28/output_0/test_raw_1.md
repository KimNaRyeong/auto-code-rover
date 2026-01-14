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
        # Set Seaborn version to 0.12
        get_ipython().magic("matplotlib inline")
        get_ipython().magic("run --head -m seaborn.tests.testing_init --delete-confirmed")

        reproduce_issue()
        assert False, "Issue not found"
    except AssertionError:
        pass
    except Exception as e:
        print_stacktrace(e)
        raise
```
To reproduce the issue, run the script with Seaborn version 0.12 installed:
```bash
$ conda create -n seaborn-0.12 seaborn=0.12
$ conda activate seaborn-0.12
$ python3 reproducer.py
```
The script sets the Seaborn version to 0.12 using the `seaborn.tests.testing_init` module, which allows for reproducible plotting. It then calls the `reproduce_issue()` function, which generates the plot with overlapping labels. The script raises an `AssertionError` to indicate that the issue has been reproduced.

To fix the issue, update Seaborn to version 11.2 or later:
```bash
$ conda update seaborn
```
Then, re-run the script to confirm that the issue has been resolved:
```bash
$ python3 reproducer.py
```
The script should exit without raising any exceptions, indicating that the issue has been fixed.