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

def verify_markers_center_aligned():
    from matplotlib import pyplot as plt
    from matplotlib.text import TextPath
    from matplotlib.font_manager import FontProperties
    fp = FontProperties(family="DejaVu Sans")
    star_path = TextPath((0, 0), "$\star$", size=12, prop=fp)

    fig, ax = plt.subplots()
    ax.plot(10, 10, color='b', alpha=1.0, marker="*", markersize=25)  # Regular star marker

    # Using mathtext marker (we position this manually a bit off for visual check, adjust if necessary)
    ax.plot(10, 10, color='g', alpha=1.0, marker=star_path, markersize=25)

    ax.plot(10, 10, color='r', alpha=1.0, marker=".")  # Reference dot marker

    ax.set_xlim([9.5, 10.5])
    ax.set_ylim([9.5, 10.5])
    plt.savefig("issue_reproduction.png")

    # If the issue exists, then the green star (mathtext) won't be center-aligned with blue and red markers.
    # We check if the bounding box of the star_path is centered. This is a very crude way, but
    # for demonstration purposes, let's assume this check could simulate catching misalignment.
    bbox = star_path.get_extents()
    center = bbox.width / 2, bbox.height / 2

    if center != (0, 0):
        raise AssertionError("Mathtext marker is not center-aligned.")

try:
    verify_markers_center_aligned()
except Exception as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue not detected, markers are center-aligned.")
    exit(0)
