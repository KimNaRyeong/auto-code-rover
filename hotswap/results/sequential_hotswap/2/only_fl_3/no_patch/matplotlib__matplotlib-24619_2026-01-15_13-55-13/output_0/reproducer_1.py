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

def test_matplotlib_color():
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib import colormaps
    
    try:
        cmap = colormaps.get_cmap('bwr_r')
        fig, ax = plt.subplots()
        x, y = np.mgrid[0:10:100j, 0:10:100j]
        v = np.abs(np.sin(x) * np.cos(y))
        c = (cmap(v[:-1, :-1]) * 255).astype(np.int64)
        ax.pcolorfast(x, y, c)

        raise AssertionError("Issue not reproduced, no ValueError raised.")
        
    except ValueError as e:
        if "RGBA values should be within 0-1 range" in str(e):
            print("Issue reproduced successfully, expected ValueError due to bug presence.")
            print_stacktrace(e)
        else:
            print("Unexpected ValueError caught.")
            print_stacktrace(e)
            exit(1)
        
    except AssertionError as e:
        print("AssertionError raised, this means the issue was not present. Unexpected outcome.")
        print_stacktrace(e)
        exit(1)

    except Exception as e:
        print("Unexpected exception occurred.")
        print_stacktrace(e)
        exit(1)

    else:
        print("No exception was raised, this typically indicates that the issue has been fixed.")
        exit(0)

if __name__ == "__main__":
    test_matplotlib_color()
