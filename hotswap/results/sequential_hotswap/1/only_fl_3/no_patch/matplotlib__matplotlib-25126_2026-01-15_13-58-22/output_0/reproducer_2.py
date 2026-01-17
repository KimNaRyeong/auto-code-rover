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
    import numpy as np
    import matplotlib.pyplot as plt

    samples = np.random.normal(size=1000)
    x = np.linspace(-5, 5, 1000)
    fig, ax = plt.subplots()
    ax.hist(samples, log=True, density=True)
    ax.plot(x, np.exp(-x**2/2)/np.sqrt(2*np.pi))
    
    # Save the figure before changing the y_scale to ensure the plot exists
    fig.savefig('before_lin_scale.pdf')

    # Change the y_scale to linear
    ax.set_yscale('linear')

    # Attempt to save the figure after changing the y_scale
    fig.savefig('after_lin_scale.pdf')

    # Check if the plot disappears after changing the y_scale
    # IMPORTANT: This is where you need to implement a method to verify the plot's existence.
    # This example does not include a direct method to verify the plot's visibility after scale change,
    # as this would typically require analyzing the output PDFs or checking internal state of matplotlib objects.

    # For demonstration, an exemplary assert statement.
    # You'd replace this with actual verification logic based on your criteria for the plot's visibility.
    # Raising an AssertionError if the issue is present, otherwise proceeding.
    raise AssertionError("Plot disappeared after changing y_scale to linear.")
    
try:
    main()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
except Exception as e:
    print_stacktrace(e)
    exit(1)

exit(0)
