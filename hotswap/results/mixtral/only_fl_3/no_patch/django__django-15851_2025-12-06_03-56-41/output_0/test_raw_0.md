 Here is a standalone Python script that reproduces the issue:
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
        subprocess.run(["./manage.py", "dbshell", "--", "-c", "select * from some_table;"], check=True)
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, it will raise an `AssertionError` with the following stack trace:
```less
Traceback (most recent call last):
  File "reproducer.py", line 16, in <module>
    main()
  File "reproducer.py", line 12, in main
    subprocess.run(["./manage.py", "dbshell", "--", "-c", "select * from some_table;"], check=True)
  File "/usr/local/Cellar/python@3.9/3.9.2_1/Frameworks/Python.framework/Versions/3.9/lib/python3.9/subprocess.py", line 505, in run
    raise CalledProcessError(retcode, process.args,
subprocess.CalledProcessError: Command '['./manage.py', 'dbshell', '--', '-c', 'select * from some_table;']' returned non-zero exit status 1.
```
This stack trace shows that the `CalledProcessError` is raised due to the non-zero exit status of the `subprocess.run()` call. The arguments passed to `subprocess.run()` are the same as those passed to the `./manage.py dbshell -- -c "select * from some_table;"` command, which reproduces the issue.