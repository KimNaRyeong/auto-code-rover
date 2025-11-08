import matplotlib.pyplot as plt
import matplotlib

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
    plt.rcParams['figure.autolayout'] = True  # Set figure.autolayout to True
    fig, axes = plt.subplots(ncols=2)
    fig.tight_layout(w_pad=10)  # Should insert padding of 10 points

    # Check if the padding is actually inserted
    fig.canvas.draw()
    inches_width = fig.get_figwidth()
    pixels_width = int(inches_width * fig.dpi)
    assert axes[0].get_window_extent().width > pixels_width / 2, "No padding was inserted"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
