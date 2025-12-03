 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
import subprocess
from urllib.request import urlopen

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def run_server():
    args = ['python', 'manage.py', 'runserver']
    subprocess.check_call(args)

def test_head_request():
    args = ['curl', '-iX', 'HEAD', 'http://127.0.0.1:8000/']
    curl_proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    output = curl_proc.communicate()[0].decode('utf-8')
    headers, body = output.split('\r\n\r\n', 1)
    assert '\r\n' not in body, 'Response body should not be present for HEAD request'

if __name__ == '__main__':
    run_server()
    try:
        test_head_request()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
To run the script, execute `python3 reproducer.py` in the root directory of the Django project. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed to the console. If the issue is fixed, the script will exit with code 0.

Note: This script assumes that `curl` is installed on the system and that the `manage.py` script is located in the root directory of the Django project.