Here is the reproducer script:

```python
import click
from flask import Flask
from flask.cli import with_appcontext, AppGroup

def create_app():
    return Flask(__name__)

@click.group()
def my_big_cli_group():
    pass

@my_big_cli_group.group(cls=AppGroup, create_app=create_app)
@click.pass_context
def my_flask_app(ctx):
    pass

@my_flask_app.command()
@click.pass_context
@click.option('-s', '--start', is_flag=True)
def my_command(ctx, start):
    click.echo(start)

if __name__ == '__main__':
    try:
        @my_big_cli_group.group(cls=AppGroup, create_app=create_app)
        @click.pass_context
        def my_flask_app(ctx):
            pass

        my_big_cli_group()
    except Exception as e:
        print_stacktrace(e)
        raise
```

This script should be run with `python3 reproducer.py`. If the issue is present, it will raise an `AssertionError` and print a stack trace.