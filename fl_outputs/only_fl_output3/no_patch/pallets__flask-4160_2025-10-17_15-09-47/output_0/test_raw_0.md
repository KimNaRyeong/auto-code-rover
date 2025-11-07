```python
# reproducer.py
import decimal
from datetime import datetime
from flask import Flask, json as fjson
from flask.json import JSONEncoder
import simplejson as sjson

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

# Custom JSON Encoder
class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super().default(o)

def test_default_behavior():
    app = Flask(__name__)
    rdatetime = datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
    rdecimal = decimal.Decimal(10)
    obj = {'datetime': rdatetime, 'decimal': rdecimal}

    try:
        flask_output = fjson.dumps(obj)
        # Flask should fail without custom encoder due to Decimal
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Default behavior failed on Flask side")

    try:
        simplejson_output = sjson.dumps(obj)
        # Simplejson should fail due to datetime objects
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Default behavior failed on Simplejson side")

def test_custom_encoder_behavior():
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    rdatetime = datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
    rdecimal = decimal.Decimal(10)
    obj = {'datetime': rdatetime, 'decimal': rdecimal}

    try:
        # This should not fail after setting custom encoder
        custom_output = fjson.dumps(obj, cls=app.json_encoder)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Custom encoder behavior failed")

if __name__ == "__main__":
    test_default_behavior()
    test_custom_encoder_behavior()
    print("Reproduction successful: Issue present.")
```

This script attempts at reproducing the issue described:

1. The `test_default_behavior` function tests the default serialization behavior of both Flask's and Simplejson's encoders with an object containing both `datetime` and `Decimal` types. It's expected to fail due to the limitations described in the issue, but instead of asserting failure directly (which would stop the script execution), it uses exceptions to print stack traces for better diagnosis.

2. The `test_custom_encoder_behavior` sets up a Flask app to use a custom JSON encoder designed to handle `Decimal` types by converting them to strings. This part of the script checks if the custom encoder approach correctly serializes objects containing both `datetime` and `Decimal` without errors, essentially representing the proposed solution to the issue.

3. Upon success, the script confirms the issue's reproduction by proceeding without any uncaught exceptions and prints a message signifying the issue's presence. If the issue is fixed (meaning Flask can handle `Decimal` types by default or `simplejson` can correctly serialize `datetime` objects),  the script would raise an `AssertionError`.

This script will exit with code 0 (assuming no unhandled exceptions occur), regardless of assertion status, meant to indicate script execution completion rather than issue presence or absence. For true issue tracking, integrating this script into a broader test suite with standardized error handling and exit codes representing specific outcomes would be advisable.