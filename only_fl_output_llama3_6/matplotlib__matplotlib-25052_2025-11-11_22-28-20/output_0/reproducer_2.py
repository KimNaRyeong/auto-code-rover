import matplotlib.pyplot as plt
from matplotlib import axes, transforms

def main():
    fig, ax = plt.subplots()
    table = ax.table(cellText=[['A', 'B'], ['1', '2']], loc='center')
    bbox = transforms.Bbox.from_bounds(0.5, 0.5, 0.7, 0.7)
    try:
        table.set_bbox(bbox)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Error occurred"

    plt.show()

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

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if e.code != 0:
            raise
    except Exception as e:
        print_stacktrace(e)
        exit(1)
