 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import sys
import traceback

def print_stacktrace(e):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def f():
    print(django.__version__)

if __name__ == "__main__":
    try:
        import django
        exec("f()")
    except Exception as e:
        print_stacktrace(e)
        assert False, "An exception should not be raised here."
    else:
        print("The issue is fixed.")
        sys.exit(0)
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` with a stack trace, indicating that the issue is present. The relevant lines of the stack trace should be similar to the following:
```ruby
Traceback (most recent call last):
  File "reproducer.py", line 18, in <module>
    exec("f()")
  File "<string>", line 4, in f
NameError: name 'django' is not defined
```
To fix the issue, you can modify the `exec` call in `reproducer.py` to pass an empty dictionary as the second argument, which will serve as the global namespace for the executed code:
```python
exec("f()", {})
```
With this modification, the script should print "The issue is fixed." and exit with code 0.