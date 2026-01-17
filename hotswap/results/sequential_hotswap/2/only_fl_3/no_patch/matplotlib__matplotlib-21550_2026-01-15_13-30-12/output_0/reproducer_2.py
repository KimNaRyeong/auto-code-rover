import matplotlib.pyplot as plt
import numpy as np
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

def generate_plot():
    # This is a placeholder function to generate the plot that could be affected by the issue
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plt.plot(x, y)
    plt.title("Sine Wave Example")
    # Saving the plot to a file instead of displaying it
    plt.savefig('plot_output.png')
    plt.close()

def compare_plots():
    # Placeholder for comparing saved plot images
    # In a real scenario, you would load the images and compare them pixel by pixel or use a more sophisticated comparison method
    # For illustrative purposes, let's just pretend we did a comparison and found an issue
    return False

def main():
    try:
        generate_plot()
        if not compare_plots():
            raise AssertionError("Plot output differs from the expected result.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
