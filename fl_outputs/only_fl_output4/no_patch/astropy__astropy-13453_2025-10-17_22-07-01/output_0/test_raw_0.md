Below is the `reproducer.py` script designed to reproduce the issue described. This script will generate a table and attempt to write it to HTML using the specified formats for the columns. It then checks whether the formatted output matches the expected output, raising an `AssertionError` if the formatting was ignored (indicating the issue is present).

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

def test_html_formatting():
    from astropy.table import Table
    from io import StringIO

    # generate table
    t = Table([(1.23875234858e-24, 3.2348748432e-15), (2, 4)], names=('a', 'b'))
    
    # expected formatted values for column "a"
    expected_a_values = ["1.24e-24", "3.23e-15"]
    
    # Write table to HTML with specified formats
    with StringIO() as sp:
        t.write(sp, format="html", formats={"a": lambda x: f"{x:.2e}"})
        html_output = sp.getvalue()
    
    # Check if the formatted values for column "a" are present in the HTML output
    all_present = all(expected_val in html_output for expected_val in expected_a_values)
    
    if not all_present:
        raise AssertionError("HTML output did not respect formatting for column 'a'.")

if __name__ == "__main__":
    try:
        test_html_formatting()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("No formatting issue detected, all tests passed.")
        exit(0)
```

This script checks specifically for the presence of the correctly-formatted values in the HTML output. If the format is not applied, and the values are found in their original, non-formatted form, an `AssertionError` is raised, pinpointing the presence of the reported issue.