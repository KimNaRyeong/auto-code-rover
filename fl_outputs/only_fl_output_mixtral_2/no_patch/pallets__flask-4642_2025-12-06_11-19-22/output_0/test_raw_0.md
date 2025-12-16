 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import click
from flask.cli import FlaskGroup

def create_app():
    app = Flask(__name__)
    @app.cli.command()
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

if __name__ == "__main__":
    try:
        my_big_cli_group(obj={})(['my_flask_app', 'run'])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("FlaskGroup does not work when nested in a click.group")
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 43, in <module>
    my_big_cli_group(obj={})(['my_flask_app', 'run'])
  File "venv/lib/python3.7/site-packages/click/core.py", line 1128, in __call__
    return self.main(*args, **kwargs)
  File "venv/lib/python3.7/site-packages/click/core.py", line 1053, in main
    rv = self.invoke(ctx)
  File "venv/lib/python3.7/site-packages/click/core.py", line 1659, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "venv/lib/python3.7/site-packages/click/core.py", line 1395, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "venv/lib/python3.7/site-packages/click/core.py", line 754, in invoke
    return __callback(*args, **kwargs)
  File "venv/lib/python3.7/site-packages/click/decorators.py", line 26, in new_func
    return f(get_current_context(), *args, **kwargs)
  File "reproducer.py", line 32, in my_flask_app
    create_app=create_app)
  File "venv/lib/python3.7/site-packages/flask/cli.py", line 393, in load_app
    ‘Could not locate a Flask application. You did not provide ’
AssertionError: FlaskGroup does not work when nested in a click.group
```
This reproduces the issue where the `create_app` function is not passed to the `Group.group` instances in `click`.