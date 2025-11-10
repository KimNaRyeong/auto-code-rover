Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
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

        plt.show()

        # Check if the labels are overlapping
        fig = g.fig
        axes_list = fig.axes
        texts = [item.get_text() for sublist in [ax.texts for ax in axes_list] for item in sublist]
        max_widths = [max([t.get_window_extent().width for t in ax.texts]) for ax in axes_list]
        assert all(max_width < 0.5 * ax.bbox.width for ax, max_width in zip(axes_list, max_widths)), "Overlapping labels detected"
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```
This script will generate a plot using seaborn 0.12 and then check if the labels are overlapping by checking the width of the text labels against the width of the axes. If overlapping labels are detected, it will raise an `AssertionError` with a stack trace.

Please make sure that you have matplotlib installed in your environment before running this script.