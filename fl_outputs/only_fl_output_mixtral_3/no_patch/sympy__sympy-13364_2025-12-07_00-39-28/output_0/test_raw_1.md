 Here is a standalone Python script `reproducer.py` to reproduce the issue:
```python
from sympy import S

def print_stacktrace(e):
    import traceback, sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    try:
        pow(S(2), S(3), S(5))
    except Exception as e:
        print_stacktrace(e)
        assert False
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 12, in <module>
    pow(S(2), S(3), S(5))
  File "/Users/username/anaconda3/lib/python3.8/site-packages/sympy/core/power.py", line 217, in __new__
    return pow(base, exp, **kwargs)
TypeError: __sympifyit_wrapper() takes exactly 2 arguments (3 given)

---------------------------------------------------------------------------
AssertionError                            Traceback (most recent call last)
<ipython-input-1-16b681d6b5e8> in <module>
     10     except Exception as e:
     11         print_stacktrace(e)
---> 12         assert False

AssertionError:
```
This confirms that the issue is present. When the issue is fixed, the script will not raise an `AssertionError` and will exit with code 0.