# reproducer.py
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
        from astropy.table import QTable
        import astropy.units as u
        import sys
        tbl = QTable({'wave': [350, 950] * u.nm, 'response': [0.7, 1.2] * u.count})

        # Try to write table with header rows for ascii.rst format
        tbl.write(sys.stdout, format="ascii.rst", header_rows=["name", "unit"])
        print("Issue fixed, exiting with code 0.")
        sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        # If the specific 'TypeError' is encountered, it means the issue is present
        assert isinstance(e, TypeError) and str(e).endswith("got an unexpected keyword argument 'header_rows'"), "Unexpected failure!"
        
if __name__ == "__main__":
    main()
