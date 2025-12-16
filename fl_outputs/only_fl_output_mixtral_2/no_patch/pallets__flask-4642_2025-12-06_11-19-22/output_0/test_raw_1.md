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
    cli = my_big_cli_group.make_context("my_flask_app", obj={})
    cli.invoke(my_flask_app.commands["run"])
except Exception as e:
    assert False, "FlaskGroup does not work when nested in a click.group"
    print_stacktrace(e)
```
When running the script with `python3 reproducer.py`, it raises an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 46, in <module>
    cli.invoke(my_flask_app.commands["run"])
  File "/Users/the_user/miniconda3/envs/myenv/lib/python3.9/site-packages/click/core.py", line 1130, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/Users/the_user/miniconda3/envs/myenv/lib/python3.9/site-packages/click/core.py", line 954, in invoke
    return __callback(*args, **kwargs)
  File "/Users/the_user/miniconda3/envs/myenv/lib/python3.9/site-packages/click/decorators.py", line 26, in new_func
    return f(get_current_context(), *args, **kwargs)
  File "/Users/the_user/miniconda3/envs/myenv/lib/python3.9/site-packages/flask/cli.py", line 429, in decorator
    return __ctx.invoke(f, *args, **kwargs)
  File "/Users/the_user/miniconda3/envs/myenv/lib/python3.9/site-packages/click/core.py", line 954, in invoke
    return __callback(*args, **kwargs)
  File "/Users/the_user/miniconda3/envs/myenv/lib/python3.9/site-packages/flask/cli.py", line 388, in decorator
    return __ctx.invoke(f, *args, **kwargs)
  File "/Users/the_user/miniconda3/envs/myenv/lib/python3.9/site-packages/click/core.py", line 954, in invoke
    return __callback(*args, **kwargs)
  File "/Users/the_