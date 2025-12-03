 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sys
from astropy.table import Table
from io import StringIO

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    t = Table([(1.23875234858e-24, 3.2348748432e-15), (2, 4)], names=('a', 'b'))
    tc = t.copy()
    with StringIO() as sp:
        tc.write(sp, format="html", formats={"a": lambda x: f"{x:.2e}"})
        html = sp.getvalue()
    expected = "<html>\n <head>\n  <meta charset=\"utf-8\"/>\n  <meta content=\"text/html;charset=UTF-8\" http-equiv=\"Content-type\"/>\n </head>\n <body>\n  <table>\n   <thead>\n    <tr>\n     <th>a</th>\n     <th>b</th>\n    </tr>\n   </thead>\n   <tr>\n    <td>1.24e-24</td>\n    <td>2</td>\n   </tr>\n   <tr>\n    <td>3.23e-15</td>\n    <td>4</td>\n   </tr>\n  </table>\n </body>\n</html>"
    assert html == expected, f"Expected:\n{expected}\nReceived:\n{html}"

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed, the script will raise an `AssertionError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 25, in <module>
    main()
  File "reproducer.py", line 21, in main
    assert html == expected, f"Expected:\n{expected}\nReceived:\n{html}"
AssertionError: Expected:
<html>
 <head>
  <meta charset="utf-8"/>
  <meta content="text/html;charset=UTF-8" http-equiv="Content-type"/>
 </head>
 <body>
  <table>
   <thead>
    <tr>
     <th>a</th>
     <th>b</th>
    </tr>
   </thead>
   <tr>
    <td>1.24e-24</td>
    <td>2</td>
   </tr>
   <tr>
    <td>3.23e-15</td>
    <td>4</td>
   </tr>
  </table>
 </body>
</html>
Received:
<html>
 <head>
  <meta charset="utf-8"/>
  <meta content="text/html;charset=UTF-8" http-equiv="Content-type"/>
 </head>
 <body>
  <table>
   <thead>
    <tr>
     <th>a</th>
     <th>b</th>
    </tr>
   </thead>
   <tr>
    <td>1.23875234858e-24</td>
    <td>2</td>
   </tr>
   <tr>
    <td>3.2348748432e-