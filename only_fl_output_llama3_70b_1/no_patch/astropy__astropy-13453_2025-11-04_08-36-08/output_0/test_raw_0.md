Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
```python
import astropy.table as Table
from io import StringIO
import sys

# generate table
t = Table([(1.23875234858e-24, 3.2348748432e-15), (2, 4)], names=('a', 'b'))
tc = t.copy()  # copy table

# print HTML table with "a" column formatted to show 2 decimal places
with StringIO() as sp:
    tc.write(sp, format="html", formats={"a": lambda x: f"{x:.2e}"})
    html_output = sp.getvalue()

# Check if the formatting is respected
if '1.23875234858e-24' in html_output or '3.2348748432e-15' in html_output:
    raise AssertionError("HTML table output does not respect the supplied formats")

print("Issue is fixed")
sys.exit(0)
```
This script will raise an `AssertionError` if the issue is present and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.

You can run this script using `python3 reproducer.py`.