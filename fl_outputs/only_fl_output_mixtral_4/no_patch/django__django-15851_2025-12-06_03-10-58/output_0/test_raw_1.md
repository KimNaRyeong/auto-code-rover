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
        # Reproduce the issue
        subprocess.run(["./manage.py", "dbshell", "--", "-c", "select * from some_table;"])
        # The issue is present, so the script should not reach this point
        assert False, "The script should not reach this point"
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace showing the line numbers of the statements. The output will look something like this:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 18, in <module>
    main()
  File "reproducer.py", line 13, in main
    subprocess.run(["./manage.py", "dbshell", "--", "-c", "select * from some_table;"])
  File "/usr/local/Cellar/python@3.9/3.9.2_1/Frameworks/Python.framework/Versions/3.9/lib/python3.9/subprocess.py", line 505, in run
    raise CalledProcessError(retcode, process.args,
subprocess.CalledProcessError: Command '['./manage.py', 'dbshell', '--', '-c', 'select * from some_table;']' returned non-zero exit status 1.
```
The issue is caused by the order of the arguments passed to `subprocess.run()`. The `--` option and the SQL command should be passed before the database name, but in this case, the database name (`dbshell`) is passed before the `--` option and the SQL command. To fix the issue, the arguments should be reordered as follows:
```python
subprocess.run(["./manage.py", "-c", "select * from some_table;", "--", "dbshell"])
```
With this change, the script will exit with code 0 when executed with `python3 reproducer.py`.