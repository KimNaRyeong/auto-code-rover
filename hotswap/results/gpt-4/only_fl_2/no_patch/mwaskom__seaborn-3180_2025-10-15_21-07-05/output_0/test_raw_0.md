```python
# reproducer.py

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

def check_for_overlap(figure) -> bool:
    """A simplified overlap detection logic which might not catch all edge cases but serves for this demonstration."""
    for ax in figure.axes:
        bbox_children = [child.get_window_extent() for child in ax.get_children() if hasattr(child, 'get_window_extent')]
        for i, bbox_a in enumerate(bbox_children[:-1]):
            for bbox_b in bbox_children[i+1:]:
                if bbox_a.overlaps(bbox_b):
                    return True
    return False

def reproduce_issue():
    sns.set_context("paper")
    sns.set_style("white")

    data = (sns.load_dataset('iris').set_index('species') * 1e7).reset_index()
    g = sns.relplot(data=data, x='sepal_length', y='sepal_width', col='species', 
                    col_wrap=2, height=2.5, facet_kws=dict(sharex=False, sharey=False))
    g.set_titles(row_template="{row_name}", col_template="SOMEWHATLONG-{col_name}")
    for axes in g.axes.flat:
        axes.ticklabel_format(axis='both', style='scientific', scilimits=(0, 0))

    overlap_found = check_for_overlap(g)
    if overlap_found:
        raise AssertionError("Label overlap detected in seaborn relplot.")

try:
    reproduce_issue()
except Exception as e:
    print_stacktrace(e)
    exit(1)  # Exit with non-zero to indicate the presence of the issue
else:
    print("No overlap detected, issue seems to be resolved.")
    exit(0)
```

This script aims to reproduce a described issue related to label overlap in seaborn's `relplot`. The `check_for_overlap` function is a basic implementation for detecting overlap between labels and may need customization based on the specifics of label overlap you're encountering. Adjustments to the logic for detecting overlaps might be necessary for a more accurate reproduction and assertive check of the issue.