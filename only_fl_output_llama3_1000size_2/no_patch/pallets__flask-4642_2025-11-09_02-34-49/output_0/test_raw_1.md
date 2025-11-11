Here is the reproducer script:

```python
import click
from flask import Flask
from flask.cli import with_appcontext, AppGroup

def create_app():
    app = Flask(__name__)
    return app

@click.group(cls=AppGroup, create_app=create_app)
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

@my_big_cli_group.group(cls=AppGroup, create_app=create_app)
@click.pass_context
def my_flask_app(ctx):
    pass

if __name__ == '__main__':
    try:
        my_big_cli_group()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected NoAppException but got another exception")
```

This script should be run with `python3 reproducer.py`.