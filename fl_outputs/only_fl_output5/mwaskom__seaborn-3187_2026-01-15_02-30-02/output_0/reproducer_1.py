import matplotlib.pyplot as plt
import seaborn as sns
import seaborn.objects as so
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

def check_legend_format():
    plt.figure()  # Ensure we have a fresh matplotlib figure
    penguins = sns.load_dataset("penguins")
    penguins["body_mass_mg"] = penguins["body_mass_g"] * 1000
    plot = so.Plot(penguins, x="bill_length_mm", y="bill_depth_mm", color="species", pointsize="body_mass_mg").add(so.Dot())
    plot.show()

    # Try to access the legend and its labels to check their format
    legend = plt.gca().get_legend()
    if legend is None:
        raise AssertionError("No legend found in the plot. Unable to check for correct legend value formatting.")

    legend_labels = [text.get_text() for text in legend.get_texts()]
    # Potential criterion for checking correct formatting, adjust as necessary
    assert legend_labels, "Legend exists but has no labels."

    # Assuming the reported issue would reflect an incorrect representation of large numbers
    # Here, a simple check for presence of scientific notation might not suffice, but it's a start
    for label in legend_labels:
        if "e" in label:
            raise AssertionError("Legend labels appear to be improperly formatted without multiplicative offset.")

def main():
    try:
        check_legend_format()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with an error code to indicate presence of issue or another error

    print("The legend values are properly formatted. The issue seems to be fixed.")
    sys.exit(0)  # Exit code 0 to indicate that the issue has been resolved

if __name__ == "__main__":
    main()
