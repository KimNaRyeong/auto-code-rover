# reproducer.py

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
    try:
        import matplotlib.pyplot as plt
        import numpy as np

        test = np.full((2, 1), -1)
        fig, ax = plt.subplots()
        im = ax.imshow(test)

        # Attempt to simulate the mouse hovering
        # Does not directly mimic UI interaction but should provoke the delta calculation
        for x in range(test.shape[1]):
            for y in range(test.shape[0]):
                try:
                    val = im.get_cursor_data((x, y))
                except Exception as e:
                    print_stacktrace(e)
                    raise AssertionError("imshow failed with identical negative values") from e
                    
        plt.close(fig)
    except AssertionError as error:
        raise
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("An unexpected error occurred") from e

if __name__ == "__main__":
    main()
