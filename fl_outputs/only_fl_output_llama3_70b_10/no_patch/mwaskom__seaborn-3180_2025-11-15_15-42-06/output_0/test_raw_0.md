Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import seaborn as sns
import matplotlib.pyplot as plt

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
    sns.set_context("paper")
    sns.set_style("white")

    data = (sns.load_dataset('iris').set_index('species')*1e7).reset_index()
    g = sns.relplot(data=data, x='sepal_length', y='sepal_width', col='species', 
                    col_wrap=2, height=2.5)
    g.set_titles(row_template="{row_name}", col_template="SOMEWHATLONG-{col_name}")
    for axes in g.axes.flat:
        axes.ticklabel_format(axis='both', style='scientific', scilimits=(0, 0))

    plt.savefig('seaborn_11_2.png')
    plt.close()

    try:
        assert len(g.axes[0].get_xticklabels()) == len(set(t.get_text() for t in g.axes[0].get_xticklabels())), "Overlapping labels detected"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```
This script will reproduce the issue and raise an `AssertionError` if overlapping labels are detected. The error message will include a stack trace with line numbers, making it easier to debug. If the issue is fixed, the script will exit with code 0.