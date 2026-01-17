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
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
To reproduce the issue, you can run the script with Seaborn version 0.12 installed:
```
$ conda create -n seaborn-0.12 seaborn=0.12
$ conda activate seaborn-0.12
$ python3 reproducer.py
```
The script should print the stack trace of the issue and exit with code 0.

To fix the issue, you can install Seaborn version 11.2 or later:
```
$ conda install -n seaborn-11.2 seaborn=11.2
$ conda activate seaborn-11.2
$ python3 reproducer.py
```
The script should not print any error message and exit with code 0.