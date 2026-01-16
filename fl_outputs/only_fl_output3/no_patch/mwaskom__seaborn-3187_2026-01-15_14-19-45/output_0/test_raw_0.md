```python
import matplotlib as mpl
import seaborn as sns
import seaborn.objects as so
from matplotlib.ticker import ScalarFormatter
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    penguins = sns.load_dataset("penguins")
    penguins["body_mass_mg"] = penguins["body_mass_g"]*1000
    plot = so.Plot(
        penguins, x="bill_length_mm", y="bill_depth_mm",
        color="species", pointsize="body_mass_mg",
    ).add(so.Dot())
    
    # Attempt to extract the legend text for validation
    ax = plot.plot().ax
    legend = ax.get_legend()
    legend_texts = [t.get_text() for t in legend.get_texts()]
    
    # Assuming the issue causes missing or incorrect multiplicative offset in legend,
    # when correct, the legend should contain strings formatted with an offset (e.g., 1e6)
    try:
        assert any(["e" in text for text in legend_texts]), \
            "Legend labels do not properly display multiplicative offset."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error status if the issue is present
    
    print("Issue not found: Legends are correctly formatted with multiplicative offset.")

if __name__ == '__main__':
    main()
```