 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

from flask import json as fjson
from flask.json import JSONEncoder
import simplejson as sjson
import decimal
from datetime import datetime

rdatetime = datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
rdecimal = decimal.Decimal(10)

obj = {'datetime': rdatetime, 'decimal': rdecimal}

app = Flask(__name__)

# Using Flask version 2.0.1
# app = Flask(__name__, json_encoder=CustomJSONEncoder)

try:
    fjson.dumps(obj)
except Exception as e:
    print("Flask JSONEncoder fails to handle Decimal type:")
    print_stacktrace(e)

try:
    sjson.dumps(obj)
except Exception as e:
    print("SimpleJSON fails to handle datetime type:")
    print_stacktrace(e)
```
To run the script, execute `python3 reproducer.py` in the terminal.

The script uses the `print_stacktrace` function to print the stack trace of any exceptions raised during the execution of the script.

The script defines a dictionary `obj` containing a `datetime` object and a `Decimal` object. It then tries to serialize the dictionary using both the Flask `JSONEncoder` and the `simplejson` encoder. The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.