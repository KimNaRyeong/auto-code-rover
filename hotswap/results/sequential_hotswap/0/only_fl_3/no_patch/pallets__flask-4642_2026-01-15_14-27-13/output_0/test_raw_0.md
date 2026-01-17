Below is a standalone Python script named `reproducer.py` that attempts to reproduce the issue as described. It simulates a CLI with nested FlaskGroup, and it will raise an `AssertionError` if the Flask application is not found as expected.

```python
import click
from flask import Flask
from flask.cli import FlaskGroup

app_name = "my_flask_app"

def create_app(info):
    return Flask(app_name)

@click.group()
def my_big_cli_group():
    pass

@my_big_cli_group.group(cls=FlaskGroup, create_app=create_app)
def my_flask_app():
    pass

@my_flask_app.command()
def run():
    click.echo("Running app...")

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

def test_app_group():
    from flask.cli import NoAppException
    try:
        # Execute the "run" command in a test context
        runner = app.test_cli_runner()
        result = runner.invoke(my_flask_app, ["run"])
        # The following line should not be reached if the issue is present
        assert "Running app..." in result.output, "App did not run as expected."
    except NoAppException as e:
        print_stacktrace(e)
        raise AssertionError("Flask application not found.")

if __name__ == '__main__':
    test_app_group()
```

This script defines a CLI with a nested Flask application group. It tries to emulate the issue described in your message by setting up a CLI environment and invoking a command that would normally start the Flask application. If the Flask application is not found and a `NoAppException` is raised, it prints a detailed stack trace and raises an `AssertionError`. If the script executes correctly without raising exceptions (which would only happen if the described issue is fixed), it'll not explicitly declare success but instead, won't raise an assertion or print a stack trace.

Note: Before running this script, ensure you have Flask and Click installed in your environment, and adjust any specific details to fit your actual environment if necessary.