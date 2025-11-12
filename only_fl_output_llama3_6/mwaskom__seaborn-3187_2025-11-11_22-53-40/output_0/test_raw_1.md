Here is the reproducer script:

```python
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np

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
    penguins = sns.load_dataset("Penguins")
    penguins["body_mass_mg"] = penguins["body_mass_g"]*1000
    fig, ax = plt.subplots()
    sns.scatterplot(x="bill_length_mm", y="bill_depth_mm", hue="species", data=penguins, ax=ax, size="body_mass_mg")
    
    formatter = ScalarFormatter(useOffset=True)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(formatter)

    try:
        plt.show()
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script will create a scatter plot using seaborn and matplotlib. It sets the major formatter for both x and y axes to use offsets, which should reproduce the issue you described.