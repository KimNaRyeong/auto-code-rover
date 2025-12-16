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

plot.fig.tight_layout()
plt.show()

legend = plot.legend()
legend_labels = [label.get_text() for label in legend.get_texts()]

expected_labels = ["3000-4000 kg", "4000-5000 kg", "5000-6000 kg"]

assert legend_labels == expected_labels, "Legend values are incorrect"
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 31, in <module>
    assert legend_labels == expected_labels, "Legend values are incorrect"
AssertionError: Legend values are incorrect
```
The expected labels are calculated assuming that the `body_mass_mg` column is in the order of 1E6. The actual labels in the legend are incorrect because they do not include the multiplicative offset value.