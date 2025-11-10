import matplotlib.pyplot as plt
import os

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

def test_constrained_layout():
    fig, ax_arr = plt.subplots(2, 2, figsize=(3, 3), layout="constrained")
    fig.suptitle("suptitle that is clearly too long in this case", wrap=True)
    ax_arr[1, 0].set_title("axes title that is too long for the size", wrap=True)
    plt.savefig("test.png")

try:
    test_constrained_layout()
    img = plt.imread("test.png")
    # Assuming a reasonable image height threshold
    if img.shape[0] < 400:  # adjust this value according to your needs
        raise AssertionError("Constrained layout issue is present. The title is not fully visible.")
except Exception as e:
    print_stacktrace(e)
    exit(1)  # Exit with code 1 if an exception occurs
else:
    os.remove("test.png")  # Remove the generated image file
exit(0)  # Exit with code 0 if no issue is present
