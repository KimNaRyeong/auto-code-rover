 Here is a standalone python file `reproducer.py` to reproduce the issue:
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
               color="species", pointsize="body_mass_mg",)
plot.add(so.Dot())

ax = plot.finish()
ax.set_ylim(0, 0.07)
ax.set_xlim(30, 55)

legend = ax.legend()
legend_labels = [f"{l.get_text()} ({l.get_unit()})" for l in legend.get_texts()]

expected_labels = ["Adelie (1E+06)", "Chinstrap (1E+06)", "Gentoo (1E+06)"]
assert legend_labels == expected_labels, "Legend values are wrong"

plt.show()
```
The script sets the expected legend labels to check if the issue is present. If the issue is fixed, the script will not raise an `AssertionError` and will exit with code 0. If the issue is present, the script will raise an `AssertionError` and print a stack trace.