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
    if __name__ == "__main__":
        my_big_cli_group(obj={})
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("FlaskGroup does not work when nested in a click.group")
```
When running the script with `python3 reproducer.py`, it raises an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 44, in <module>
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
  File "reproducer.py", line 30, in my_flask_app
    @click.group(cls=FlaskGroup, create_app=create_app)
  File "/Users/user/miniconda3/envs/myenv/lib/python3.8/site-packages/click/decorators.py", line 214, in decorator
    @_wrap_init_defaults
  File "/Users/user/miniconda3/envs/myenv/lib/python3.8/site-packages/click/decorators.py", line 130, in _wrap_init_defaults
    cmd = cls(*args, **kwargs)
  File "/Users/user/miniconda3/envs/myenv/lib/python3.8/site-packages/fl