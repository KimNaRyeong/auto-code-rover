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
        from cartopy.crs import PlateCarree
        from cartopy.mpl.geoaxes import GeoAxes
        from mpl_toolkits.axes_grid1 import AxesGrid

        fig = plt.figure()
        axes_class = (GeoAxes, dict(map_projection=PlateCarree()))
        # Attempting to create an AxesGrid with a non-default axis class
        gr = AxesGrid(fig, 111, nrows_ncols=(1, 1), axes_class=axes_class)

        # If the specified error occurs, it should do so before this line.
        # Therefore, reaching here without exceptions means the issue is absent/fixed.
        print("Issue does not manifest. Proceeding without errors.")
        # Exiting with code 0 to signify the absence of the reported issue.
        exit(0)

    except Exception as e:
        print_stacktrace(e)
        # Raising AssertionError to indicate presence of the specified issue.
        raise AssertionError("Issue with creating AxisGrid with non-default axis class encountered.")

if __name__ == "__main__":
    main()
