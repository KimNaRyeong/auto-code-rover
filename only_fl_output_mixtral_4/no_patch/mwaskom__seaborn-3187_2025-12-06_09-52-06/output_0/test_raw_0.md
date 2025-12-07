 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import seaborn as sns
import seaborn.objects as so
import matplotlib.pyplot as plt

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

penguins = sns.load_dataset("Penguins")
penguins["body_mass_mg"] = penguins["body_mass_g"]*1000

plot = so.Plot(penguins, x="bill_length_mm", y="bill_depth_mm",
               color="species", pointsize="body_mass_mg",
              ).add(so.Dot())

try:
    plot.legend(title="body_mass_mg")
    plt.show()
except AssertionError:
    print_stacktrace(e)
    raise

assert plot.legend().get_title().get_text() == "body_mass_mg [1000*]", "Legend title is incorrect"
```
The script loads the `Penguins` dataset from Seaborn, multiplies the `body_mass_g` column by 1000 to create the `body_mass_mg` column, and then creates a scatter plot with the `so.Plot` and `so.Dot` functions. The legend title is set to "body\_mass\_mg".

The script then checks the title of the legend and raises an `AssertionError` if it is not "body\_mass\_mg [1000\*]". If the script runs without raising an exception, it means that the issue has been fixed.