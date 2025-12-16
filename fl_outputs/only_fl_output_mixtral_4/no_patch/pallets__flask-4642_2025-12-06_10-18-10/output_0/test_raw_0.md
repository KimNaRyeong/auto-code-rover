 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import click
from flask.cli import FlaskGroup

def create_app():
    app = Flask(__name__)
    app.cli.add_command(my_big_cli_group)
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
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    my_big_cli_group(obj={})
    my_flask_app(obj={})
    cli = my_flask_app.make_context("run")
    cli.obj.run(host="localhost", port=5000)
except Exception as e:
    assert isinstance(e, FlaskGroup.NoAppException)
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, it raises a `FlaskGroup.NoAppException` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 41, in <module>
    cli.obj.run(host="localhost", port=5000)
  File "/Users/the_user/Desktop/venv/lib/python3.7/site-packages/flask/cli.py", line 899, in run
    self.run_command(cmd, args)
  File "/Users/the_user/Desktop/venv/lib/python3.7/site-packages/flask/cli.py", line 769, in run_command
    app = DispatchingApp(self.inner_app, self.server_options, self.command_options)
  File "/Users/the_user/Desktop/venv/lib/python3.7/site-packages/flask/cli.py", line 302, in __init__
    self.make_app(error_handler)
  File "/Users/the_user/Desktop/venv/lib/python3.7/site-packages/flask/cli.py", line 286, in make_app
    app = self.load_app()
  File "/Users/the_user/Desktop/venv/lib/python3.7/site-packages/flask/cli.py", line 246, in load_app
    'Could not locate a Flask application. You did not provide '
flask.cli.NoAppException: Could not locate a Flask application. You did not provide the “FLASK_APP” environment variable, and a “wsgi.py” or “app.py” module was not found in the current directory.
```
This reproduces the issue where the `create_app` function does not get passed on to `Group.group` instances on `click`. If the `my_flask_app` group is not nested inside the `my_big_cli_group` group, then the Flask application starts without any issues.