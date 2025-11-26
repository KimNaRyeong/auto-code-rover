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

legend_titles = [t.get_text() for t in ax.legend().get_title()]
assert any("10^6" in title for title in legend_titles), "Legend titles do not contain the offset value"

print("Issue is fixed. Exiting with code 0.")
exit(0)

except AssertionError as e:
    print_stacktrace(e)
    exit(1)
