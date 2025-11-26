Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import seaborn as sns
import seaborn.objects as so
import matplotlib.pyplot as plt
import matplotlib as mpl

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

penguins = sns.load_dataset("Penguins")
penguins["body_mass_mg"] = penguins["body_mass_g"] * 1000

plot = (
    so.Plot(
        penguins, x="bill_length_mm", y="bill_depth_mm",
        color="species", pointsize="body_mass_mg",
    )
    .add(so.Dot())
)

fig, ax = plt.subplots()
plot.draw(ax)
plt.legend()

legend_texts = [t.get_text() for t in ax.legend().get_texts()]
assert any("10^6" in text for text in legend_texts), "Legend values are not correctly formatted"

print("Issue is fixed. Exiting with code 0.")
```
This script will raise an `AssertionError` if the issue is present, printing a stack trace of the error. If the issue is fixed, it will print a success message and exit with code 0.