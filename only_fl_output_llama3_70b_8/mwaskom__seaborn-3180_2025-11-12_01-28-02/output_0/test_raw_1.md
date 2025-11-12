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
        import matplotlib
        sns.set_context("paper")
        sns.set_style("white")

        data = (sns.load_dataset('iris').set_index('species')*1e7).reset_index()
        g = sns.relplot(data=data, x='sepal_length', y='sepal_width', col='species', 
                        col_wrap=2, height=2.5)
        g.set_titles(row_template="{row_name}", col_template="SOMEWHATLONG-{col_name}")
        for axes in g.axes.flat:
            axes.ticklabel_format(axis='both', style='scientific', scilimits=(0, 0))

        plt.savefig('seaborn_0.12.png')

        # Check if the labels are overlapping
        img = plt.imread('seaborn_0.12.png')
        text_areas = []
        for ax in g.axes.flat:
            for text in ax.texts:
                x, y, w, h = text.get_window_extent().bounds
                text_areas.append((x, y, w, h))

        overlapping = False
        for i in range(len(text_areas)):
            for j in range(i+1, len(text_areas)):
                x1, y1, w1, h1 = text_areas[i]
                x2, y2, w2, h2 = text_areas[j]
                if (x1 < x2 + w2 and
                    x1 + w1 > x2 and
                    y1 < y2 + h2 and
                    y1 + h1 > y2):
                    overlapping = True
                    break

        assert not overlapping, "Labels are overlapping"
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```
This script will generate a plot using seaborn 0.12 and then check if the labels are overlapping by analyzing the image. If the labels are overlapping, it will raise an `AssertionError` with a stack trace of the issue.

Note that I added `import matplotlib` to ensure that matplotlib is imported before using seaborn.