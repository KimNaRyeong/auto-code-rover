```python
import matplotlib.pyplot as plt
import seaborn as sns

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

def check_labels_overlap(axes):
    labels = []
    for ax in axes.flat:
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            bbox = label.get_window_extent()
            for other_bbox in labels:
                if bbox.overlaps(other_bbox):
                    return True
            labels.append(bbox)
    return False

def reproduce_issue():
    try:
        sns.set_context("paper")
        sns.set_style("white")

        data = (sns.load_dataset('iris').set_index('species') * 1e7).reset_index()
        g = sns.relplot(data=data, x='sepal_length', y='sepal_width', col='species',
                        col_wrap=2, height=2.5)
        g.set_titles(row_template="{row_name}", col_template="SOMEWHATLONG-{col_name}")
        for axes in g.axes.flat:
            axes.ticklabel_format(axis='both', style='scientific', scilimits=(0, 0))
        plt.draw()  # Force drawing to compute label positions
        assert not check_labels_overlap(g.axes), "Labels are overlapping"

    except AssertionError as e:
        print_stacktrace(e)
        raise  # Reraise the assertion error to exit with non-zero

    except Exception as e:  # Catch other unexpected exceptions and print their stacktrace
        print_stacktrace(e)
        exit(1)
    else:
        print("No issue found, labels are not overlapping.")

if __name__ == "__main__":
    reproduce_issue()
```

This script aims to reproduce the issue detailed, where seaborn version 0.12 shows overlapping labels in `relplot` visualizations under certain conditions. The function `check_labels_overlap` iterates over the axis labels checking for overlaps by comparing their window extents. If an overlap is detected, an `AssertionError` is raised. 

The script will exit with a status code 0 if no overlapping labels are found, implying that the issue has been fixed in the seaborn version being tested. Otherwise, it prints a stack trace of the issue caused by overlapping labels and exits with a status code that reflects the unhandled `AssertionError`.