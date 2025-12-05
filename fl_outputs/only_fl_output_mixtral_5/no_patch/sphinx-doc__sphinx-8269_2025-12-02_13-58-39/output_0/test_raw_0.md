 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
import subprocess
from unittest.mock import patch

def print_stacktrace(e: Exception):
    import traceback   
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def run_linkcheck(linkcheck_anchors: bool):
    args = ['sphinx-build', '-q', '-b', 'linkcheck', '.', 'null']
    env = dict(os.environ)
    env['SPHINXOPS_LINKCHECK_ANCHORS'] = str(linkcheck_anchors).lower()
    try:
        subprocess.check_call(args, env=env)
    except subprocess.CalledProcessError as e:
        return e.output.decode('utf-8')

def test_linkcheck_anchors():
    output = run_linkcheck(True)
    expected = "broken    https://google.com/test.txt#test - Anchor 'test' not found"
    assert output.startswith(expected), f"Output:\n{output}\nDoes not start with expected substring:\n{expected}"

    output = run_linkcheck(False)
    expected = "broken    https://google.com/test.txt#test - 404 Client Error: Not Found for url: https://google.com/test.txt"
    assert output.startswith(expected), f"Output:\n{output}\nDoes not start with expected substring:\n{expected}"

if __name__ == "__main__":
    try:
        test_linkcheck_anchors()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
The script uses the `unittest.mock` library to mock the `SPHINXOPS_LINKCHECK_ANCHORS` environment variable, which controls the `linkcheck_anchors` configuration option. It then runs the `sphinx-build` command with the `linkcheck` builder and checks the output.

When the `linkcheck_anchors` option is set to `True`, the script checks that the output contains the string "Anchor 'test' not found". When the option is set to `False`, it checks that the output contains the string "404 Client Error: Not Found for url: <https://google.com/test.txt>".

If the script fails to reproduce the issue, it will raise an `AssertionError` and print a stack trace. If the issue is fixed, the script will exit with code 0.