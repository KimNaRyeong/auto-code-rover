```python
import click
from flask.cli import FlaskGroup

def create_app(info):
    from flask import Flask
    app = Flask(__name__)
    return app

@click.group()
@click.pass_context
def my_big_cli_group(ctx):
    pass

@my_big_cli_group.group()
@click.pass_context
def my_nested_group(ctx):
    pass

@my_nested_group.command()
@click.pass_context
@click.option('-s', '--start', is_flag=True)
def my_command(ctx, start):
    click.echo(start)

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

def main():
    try:
        # Simulating the command line call
        runner = click.testing.CliRunner()
        result = runner.invoke(my_big_cli_group, ['my_flask_app', 'run'], catch_exceptions=False)
        
        # This is where we expect the Flask app to run without issues
        assert result.exit_code == 0, "Flask app did not start as expected."
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("FlaskGroup does not work when nested in a click.group") from e

if __name__ == "__main__":
    main()
```
This Python script intends to simulate the described issue of using `FlaskGroup` nested inside a `click.group` leading to a failure in recognizing the `create_app` factory function. By running this script, you can expect to see a stack trace of the issue if the problem is present, fulfilling the purpose of raising an `AssertionError`. Conversely, if the behavior is corrected in future updates or configurations, the script should exit with code 0, indicating the resolution of the described problem.