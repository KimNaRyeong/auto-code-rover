Given your requirements and aiming to ensure the script will effectively test for the described issue related to group keys in an `astropy.table.QTable`, the following Python script will raise an `AssertionError` if the issue is present (i.e., if the group keys do not include units as part of the information). It will exit with code 0 when the issue is fixed, following the details you have provided:

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

def main():
    from astropy.table import QTable
    import astropy.units as u

    try:
        tbl = QTable({"length": [1., 1., 2., 3., 1., 2.] * u.m})
        gtbl = tbl.group_by('length')

        for cols in gtbl.groups.keys:
            # Attempting to retrieve dict representation to check for unit
            col_dict = dict(cols)
            length_value = col_dict['length']
            # Check if “length” in group keys retained unit information,
            # Assuming that if the issue exists, length_value would not have 'unit' attribute
            if not hasattr(length_value, 'unit') or length_value.unit != u.m:
                raise AssertionError('Group keys are missing units.')

        print("Test passed, issue is fixed.")

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == '__main__':
    main()
```

This script encapsulates the checking logic within a `main` function and uses the provided `print_stacktrace` function to report errors clearly. When running, it checks if the keys in groups of a `QTable` object preserve the unit of measurements. If the units are missing, it catches this as an error and prints a detailed stack trace. If the issue is fixed (meaning the units are correctly included in the group keys), it will print a success message and exit with code 0 as per your specification.