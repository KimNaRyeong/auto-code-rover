# reproducer.py

def main():
    import seaborn.objects as so
    from matplotlib import pyplot as plt
    
    # Function to print the stack trace of the exception
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
    
    try:
        # Generate the plot with boolean values for colors
        so.Plot(["a", "b"], [1, 2], color=[True, False]).add(so.Bar())
        plt.show()  # Show the plot
        raise AssertionError("The issue is expected to raise a TypeError, but it didn't.")
    except TypeError as e:
        print_stacktrace(e)
        print("Issue reproduced successfully.")
    except Exception as e:
        print("An unexpected exception occurred:")
        print_stacktrace(e)
        exit(1)  # Exit with error code if the exception is unexpected

if __name__ == "__main__":
    main()
