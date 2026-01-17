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
    import matplotlib.pyplot as plt
    try:
        # This line should work without throwing an error if the issue is fixed.
        # Trying to access the default colormap should return the default defined in rcParams rather than raising an error.
        default_cmap = plt.colormaps[None]
        expected_cmap = plt.colormaps[plt.rcParams['image.cmap']]
        
        # Raising an AssertionError if the obtained colormap with None is not the expected default colormap
        assert default_cmap.name == expected_cmap.name, f"Default cmap ({default_cmap.name}) is not as expected ({expected_cmap.name})."
        print("Issue is fixed, exiting with code 0.")
    except Exception as e:
        print_stacktrace(e)
        if isinstance(e, KeyError):
            if 'None is not a known colormap name' in str(e):
                raise AssertionError("The issue is present: Directly using None with matplotlib.colormaps[] is not equivalent to accessing the default colormap.") from e

if __name__ == "__main__":
    main()
