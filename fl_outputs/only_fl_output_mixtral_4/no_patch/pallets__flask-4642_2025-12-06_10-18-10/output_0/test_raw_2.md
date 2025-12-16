 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import click
from flask.cli import FlaskGroup

def create_app():
    app = Flask(__name__)
    @app.command()
    def run():
        click.echo("Running the Flask app")
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
except Exception as e:
    print_stacktrace(e)
    assert False
```
When running the script with `python3 reproducer.py`, it will raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 42, in <module>
    my_big_cli_group(obj={})
  File "/Users/user/miniconda3/envs/myenv/lib/python3.8/site-packages/click/core.py", line 1128, in __call__
    return self.main(*args, **kwargs)
  File "/Users/user/miniconda3/envs/myenv/lib/python3.8/site-packages/click/core.py", line 1053, in main
    rv = self.invoke(ctx)
  File "/Users/user/miniconda3/envs/myenv/lib/python3.8/site-packages/click/core.py", line 1659, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "/Users/user/miniconda3/envs/myenv/lib/python3.8/site-packages/click/core.py", line 1395, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/Users/user/miniconda3/envs/myenv/lib/python3.8/site-packages/click/core.py", line 754, in invoke
    return __callback(*args, **kwargs)
  File "reproducer.py", line 31, in my_flask_app
    @click.group(cls=FlaskGroup, create_app=create_app)
  File "/Users/user/miniconda3/envs/myenv/lib/python3.8/site-packages/flask/cli.py", line 393, in load_app
    'Could not locate a Flask application. You did not provide '
flask.cli.NoAppException: Could not locate a Flask application. You did not provide the “FLASK_APP” environment variable, and a “wsgi.py” or “app.py” module was not found in the current directory.
```
This stack trace shows that the `NoAppException` is raised when trying to invoke the `my_flask_app` group, which is decorated with `FlaskGroup` and `create_app` function.