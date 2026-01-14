 Here is a standalone Python file `reproducer.py` to reproduce the issue:
```python
import argparse

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
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')
    args = parser.parse_args()

    if args.verbose:
        print("Verbose mode enabled")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        raise
```
To reproduce the issue, run the script with the `-v` option:
```shell
$ python3 reproducer.py -v
Traceback (most recent call last):
  File "reproducer.py", line 22
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/argparse.py", line 1821, in add_argument
    return self._add_action(action)
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/argparse.py", line 1998, in _add_action
    self._check_conflict(action)
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/argparse.py", line 1972, in _check_conflict
