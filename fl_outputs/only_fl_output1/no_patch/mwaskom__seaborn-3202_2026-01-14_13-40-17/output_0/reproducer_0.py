# reproducer.py

def main():
    try:
        import seaborn as sns
        import seaborn.objects as so
        
        # Load the dataset and drop NaN values
        penguins = sns.load_dataset("penguins").dropna()
        
        # Attempt to create a plot using seaborn's object-oriented interface
        (
            so.Plot(penguins, x="sex", y="bill_depth_mm")
            .add(so.Dots())
            .facet(col="species", row="island")
        )

        # If the plot creation passed without errors, the issue is not present
        print("No issue detected. Exiting with code 0.")
    except Exception as e:
        # If an exception is caught, print the stack trace
        print_stacktrace(e)
        # Assert to ensure an AssertionError is raised when an issue is detected
        assert False, "The issue is present."

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

if __name__ == "__main__":
    main()
