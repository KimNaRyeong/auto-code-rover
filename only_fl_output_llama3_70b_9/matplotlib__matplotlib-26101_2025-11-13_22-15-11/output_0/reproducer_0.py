import matplotlib.pyplot as plt
import numpy as np

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

def test_center_alignment():
    fig, ax = plt.subplots()
    ax.plot(10, 10, color='b', alpha=1.0, marker="*", markersize=25)
    ax.plot(10, 10, color='g', alpha=1.0, marker="$\star$", markersize=25)
    ax.plot(10, 10, color='r', alpha=1.0, marker=".")
    
    # Check if the star marker is center-aligned
    x, y = 10, 10
    star_bbox = ax.transData.transform([x, y])
    star_width, star_height = 25, 25  # assuming a square marker
    star_xmin, star_ymin = star_bbox[0] - star_width/2, star_bbox[1] - star_height/2
    star_xmax, star_ymax = star_bbox[0] + star_width/2, star_bbox[1] + star_height/2
    
    # Check if the mathtext star marker is center-aligned
    x, y = 10, 10
    mathtext_star_bbox = ax.transData.transform([x, y])
    mathtext_star_width, mathtext_star_height = 25, 25  # assuming a square marker
    mathtext_star_xmin, mathtext_star_ymin = mathtext_star_bbox[0] - mathtext_star_width/2, mathtext_star_bbox[1] - mathtext_star_height/2
    mathtext_star_xmax, mathtext_star_ymax = mathtext_star_bbox[0] + mathtext_star_width/2, mathtext_star_bbox[1] + mathtext_star_height/2
    
    # Assert that both markers are center-aligned
    assert np.isclose(star_xmin, star_xmax), "Star marker is not center-aligned"
    try:
        assert np.isclose(mathtext_star_xmin, mathtext_star_xmax), "Mathtext star marker is not center-aligned"
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

test_center_alignment()
plt.show()
