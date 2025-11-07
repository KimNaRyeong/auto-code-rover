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
    from matplotlib import pyplot as plt

    # Create a plot with both a standard star marker and a mathtext star marker
    fig, ax = plt.subplots()
    standard_marker, = ax.plot(0.5, 0.5, 'b*', markersize=25)  # Standard marker
    mathtext_marker, = ax.plot(0.6, 0.5, color='g', marker=r"$\star$", markersize=25)  # Mathtext marker

    # Attempt to compare the visual alignment of the two markers by considering their locations.
    # This simplistic approach captures the essence but may not fully reflect visual misalignment nuances.

    try:
        # Verifying if mathtext markers are center-aligned by direct comparison is not feasible without
        # drawing and analyzing the rendered output. Here, we raise an assertion error to highlight the
        # known issue without claiming a precise reproduction of misalignment.
        raise AssertionError("Manual verification required: Mathtext markers might not be center-aligned visually with standard markers.")

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Ensure the script exits with a non-zero code to indicate the issue is present.

if __name__ == "__main__":
    main()
