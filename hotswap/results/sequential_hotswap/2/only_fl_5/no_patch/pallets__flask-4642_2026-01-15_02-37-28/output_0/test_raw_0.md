```python
import click
from flask.cli import FlaskGroup
from flask import Flask

def create_app(info):
    return Flask(__name__)

@click.group()
@click.pass_context
def my_big_cli_group(ctx):
    """Main group of CLI commands."""
    pass

@my_big_cli_group.group(cls=FlaskGroup, create_app=create_app)
@click.pass_context
def my_flask_app(ctx):
    """Flask app group."""
    pass

@my_flask_app.command()
@click.pass_context
def run(ctx):
    """Run the flask app."""
    click.echo("Flask app running...")

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
    # Simulate calling 'my_flask_app run' command
    runner = click.testing.CliRunner()
    result = runner.invoke(my_big_cli_group, ['my_flask_app', 'run'])
    assert "Flask app running..." in result.output, "The Flask app did not run as expected."
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("The test for the FlaskGroup nested in a click.group failed.")
else:
    print("The issue seems to be fixed, as the Flask app command was executed successfully.")
```

This standalone script attempts to reproduce the issue described by:

1. Defining a `click.group` structure with nesting similar to the one provided in the issue.
2. Using `FlaskGroup` to integrate Flask command-line interface into this nested structure.
3. Simulating the execution of a command that should start the Flask app (`my_flask_app run`) using `click.testing.CliRunner`.
4. Raising an `AssertionError` if the command cannot run as expected, which indicates the presence of the described issue.
5. Printing a stack trace for any exceptions that occur during the test for better diagnosis.

The expected behavior is that the script should exit with code 0 when the problem is fixed (i.e., the Flask app runs successfully and prints "Flask app running..."), and raise an `AssertionError` (along with printing a stack trace) if the problem described in the issue persists.