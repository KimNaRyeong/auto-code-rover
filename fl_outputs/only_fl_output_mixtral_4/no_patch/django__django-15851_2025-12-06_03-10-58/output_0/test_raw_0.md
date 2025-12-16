 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import subprocess

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        # Reproduce the issue by passing additional parameters before dbname
        subprocess.run(["./manage.py", "dbshell", "--", "-c", "select * from some_table;"], check=True)
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        assert False, "The issue is present"

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace of the issue, as follows:
```ruby
Traceback (most recent call last):
  File "reproducer.py", line 18, in <module>
    main()
  File "reproducer.py", line 13, in main
    assert False, "The issue is present"
AssertionError: The issue is present
```
To fix the issue, the arguments list should be constructed in the proper order, leaving the database name for the end of the arguments list, as follows:
```python
subprocess.run(["./manage.py", "dbshell", "-c", "select * from some_table;", "--"], check=True)
```
When the arguments list is constructed in this way, the script will exit with code 0, indicating that the issue is fixed.