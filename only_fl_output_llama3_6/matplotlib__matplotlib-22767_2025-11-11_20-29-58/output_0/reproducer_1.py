import numpy as np
import matplotlib.pyplot as plt

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

def reproducer():
    try:
        import contour
        img = np.indices((100, 100))
        img = np.exp(-np.pi*(np.sum((img-50)**2,0)/20.**2))
        cs = plt.contourf(img, 50)
        cs.find_nearest_contour(20, 20, pixel=False)
    except Exception as e:
        print_stacktrace(e)
        assert False

if __name__ == "__main__":
    reproducer()
