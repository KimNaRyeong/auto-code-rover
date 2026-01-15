# reproducer.py
def main():
    try:
        import matplotlib

        # Generate a colormap using the old approach which will be deprecated
        old_cmap = matplotlib.cm.get_cmap(None)
        
        # Try to access the default colormap using the new `colormaps` approach with `None`
        new_cmap = matplotlib.colormaps[None]
        
        # Check that both approaches result in the same colormap
        assert old_cmap == new_cmap, "Mismatch in colormaps"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from None

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
    main()
