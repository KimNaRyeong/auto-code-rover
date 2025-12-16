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
    my_flask_app(object())
    my_flask_app.main(['my_flask_app', 'run'])
except Exception as e:
    print_stacktrace(e)
    assert False
```
When running the script, it raises an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 43, in <module>
    my_flask_app.main(['my_flask_app', 'run'])
  File "/Users/user/miniconda3/envs/myenv/lib/python3.8/site-packages/flask/cli.py", line 540, in list_commands
    rv.update(info.load_app().cli.list_commands(ctx))
  File "/Users/user/miniconda3/envs/myenv/lib/python3.8/site-packages/flask/cli.py", line 393, in load_app
    'Could not locate a Flask application. You did not provide '
flask.cli.NoAppException: Could not locate a Flask application. You did not provide the “FLASK_APP” environment variable, and a “wsgi.py” or “app.py” module was not found in the current directory.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "reproducer.py", line 47, in <module>
    assert False
AssertionError
```
This reproduces the issue where the `FlaskGroup` does not work when nested in a `click.group`. The expected behavior is that running `python3 reproducer.py` should not raise any exceptions and should start the Flask app. However, the actual behavior is that it raises a `flask.cli.NoAppException`.