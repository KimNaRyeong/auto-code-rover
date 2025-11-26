Here is the `reproducer.py` file that reproduces the issue:
```
import click
from flask import Flask
from flask.cli import FlaskGroup, AppGroup

def create_app():
    return Flask("my_flask_app")

@click.group()
@click.pass_context
def my_big_cli_group(ctx):
    pass

@my_big_cli_group.group(cls=FlaskGroup, create_app=create_app)
@click.pass_context
def my_flask_app(ctx):
    pass

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

try:
    my_big_cli_group(['my_flask_app', 'run'])
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected no exception"
```
This script defines a `my_big_cli_group` with a nested `my_flask_app` group that uses the `FlaskGroup` class and passes the `create_app` factory function. It then tries to run the `run` command on the `my_flask_app` group, which should start the Flask development server.

When run, this script should raise an `AssertionError` with a stack trace indicating a `flask.cli.NoAppException`, reproducing the issue described.