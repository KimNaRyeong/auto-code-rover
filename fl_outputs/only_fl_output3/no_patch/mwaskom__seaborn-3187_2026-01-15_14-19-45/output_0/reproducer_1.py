import matplotlib.pyplot as plt
import seaborn as sns
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
    # Adjusted the example to directly check for the legend issue
    penguins = sns.load_dataset("penguins")
    if penguins is None:
        raise ValueError("Penguins dataset could not be loaded. This example requires seaborn's penguins dataset.")
    
    penguins["body_mass_mg"] = penguins["body_mass_g"] * 1000
    scatter = sns.scatterplot(data=penguins, x="bill_length_mm", y="bill_depth_mm",
                              size="body_mass_mg", hue="species", legend=True)

    # Attempt to extract the legend handles and labels for validation
    handles, labels = scatter.get_legend_handles_labels()
    
    # Searching for 'e' in labels to check for scientific notation
    try:
        # It is expected that size labels (related to 'body_mass_mg') in the legend should include an 'e' for scientific notation
        assert any('e' in label for label in labels if label.replace('.', '', 1).isdigit()), "Legend labels are not correctly displaying scientific notation for large numbers."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error status if the issue is present

    print("Issue not found: Legends are correctly displaying scientific notation for large numbers.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
