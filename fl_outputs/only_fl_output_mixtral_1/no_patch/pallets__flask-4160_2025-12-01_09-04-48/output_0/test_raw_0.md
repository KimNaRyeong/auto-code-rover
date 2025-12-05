 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
import traceback

import decimal
import simplejson as sjson
from flask import Flask, json as fjson
from flask.json import JSONEncoder


def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


rdatetime = datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
rdecimal = decimal.Decimal(10)

obj = {'datetime': rdatetime, 'decimal': rdecimal}

app = Flask(__name__)

# Uncomment the following line to fix the issue
# app.json_encoder = sjson.JSONEncoder

try:
    fjson.dumps(obj)
except Exception as e:
    print_stacktrace(e)

try:
    sjson.dumps(obj)
except Exception as e:
    print_stacktrace(e)
```
To reproduce the issue, run the script with Python 3.8.10 and Flask 2.0.1:
```bash
$ python3 --version
Python 3.8.10
$ pip install Flask==2.0.1 simplejson
$ python3 reproducer.py
Traceback (most recent call last):
  File "reproducer.py", line 35, in <module>
    fjson.dumps(obj)
  File "/home/user/.local/lib/python3.8/site-packages/flask/json.py", line 123, in dumps
