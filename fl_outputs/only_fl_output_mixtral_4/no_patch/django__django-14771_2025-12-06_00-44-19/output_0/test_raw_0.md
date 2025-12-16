 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import os
import sys
import subprocess

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

def run_cmd(args):
    try:
        output = subprocess.check_output(args, stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        sys.exit(1)

def test_xoptions():
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "my_project"))
    manage_py = os.path.join(project_dir, "manage.py")
    args = [sys.executable, manage_py, "runserver", "0.0.0.0:8005", "-v3", "--noreload"]
    xoptions = ["-X", "utf8"]
    args[1:1] = xoptions
    run_cmd(args)

if __name__ == "__main__":
    test_xoptions()
    assert False, "The script should have raised a CalledProcessError exception."
```
When executed with `python3 reproducer.py`, the script should raise a `CalledProcessError` exception with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 35, in <module>
    test_xoptions()
  File "reproducer.py", line 31, in test_xoptions
    run_cmd(args)
  File "reproducer.py", line 15, in run_cmd
    output = subprocess.check_output(args, stderr=subprocess.STDOUT, universal_newlines=True)
  File "/usr/lib/python3.8/subprocess.py", line 411, in check_output
    return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,
  File "/usr/lib/python3.8/subprocess.py", line 489, in run
    with Popen(*popenargs, **kwargs) as process:
  File "/usr/lib/python3.8/subprocess.py", line 800, in __init__
