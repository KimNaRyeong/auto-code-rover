Here is a standalone Python file `reproducer.py` that reproduces the issue:

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

try:
    @my_flask_app.command()
    def run():
        print("Flask app should be running now")
except Exception as e:
    import sys
    print_stacktrace(e)
    sys.exit(1)

if __name__ == '__main__':
    try:
        my_big_cli_group()
    except AssertionError:
        print_stacktrace(Exception("Expected error"))
        sys.exit(0)
```

To reproduce the issue, run this script with Python 3.7.3 (or any other version that reproduces the issue).