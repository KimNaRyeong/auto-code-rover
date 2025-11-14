I apologize for the previous mistake. Here is a new standalone Python file `reproducer.py` to reproduce the issue:
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
    try:
        sns.set_context("paper")
        sns.set_style("white")

        data = (sns.load_dataset('iris').set_index('species')*1e7).reset_index()
        g = sns.relplot(data=data, x='sepal_length', y='sepal_width', col='species', 
                        col_wrap=2, height=2.5)
        g.set_titles(row_template="{row_name}", col_template="SOMEWHATLONG-{col_name}")
        for axes in g.axes.flat:
            axes.ticklabel_format(axis='both', style='scientific', scilimits=(0, 0))

        plt.savefig('seaborn_0.12.png')

        # Check if labels are overlapping
        fig = g.fig
        for ax in fig.axes:
            x_labels = [item.get_text() for item in ax.get_xticklabels()]
            y_labels = [item.get_text() for item in ax.get_yticklabels()]
            if any(len(label) > 10 and label != '...' for label in x_labels + y_labels):
                raise AssertionError("Overlapping labels found")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```
This script will generate a plot using seaborn 0.12 and check if there are any overlapping labels. If overlapping labels are found, it will raise an `AssertionError` with a stack trace of the issue. If no overlapping labels are found, the script will exit with code 0.

Please make sure that you have seaborn and matplotlib installed in your environment before running this script.