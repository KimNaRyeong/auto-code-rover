```python
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
    from matplotlib import pyplot as plt
    plt.figure()
    star = plt.plot(10, 10, color='b', alpha=1.0, marker="*", markersize=25)[0]
    mathtext_star = plt.plot(10, 10, color='g', alpha=1.0, marker="$\star$", markersize=25)[0]

    # Retrieving the marker paths.
    star_path = star.get_path()
    mathtext_star_path = mathtext_star.get_path()

    # Comparing the extents
    star_extents = star_path.get_extents()
    mathtext_star_extents = mathtext_star_path.get_extents()

    try:
        assert star_extents.width == mathtext_star_extents.width, "Markers width does not match"
        assert star_extents.height == mathtext_star_extents.height, "Markers height does not match"
        assert star_extents.x0 == mathtext_star_extents.x0, "Markers x-alignment does not match"
        assert star_extents.y0 == mathtext_star_extents.y0, "Markers y-alignment does not match"
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        print("All markers are properly aligned.")

if __name__ == "__main__":
    try:
        test_center_alignment()
    except AssertionError:
        exit(1)
    else:
        exit(0)
```