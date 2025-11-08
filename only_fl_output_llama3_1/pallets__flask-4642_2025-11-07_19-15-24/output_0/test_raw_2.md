Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import click
from flask import Flask
from flask.cli import with_appcontext, AppGroup

def create_app():
    app = Flask(__name__)
    return app

@click.group()
def my_big_cli_group():
    pass

@my_big_cli_group.command(cls=AppGroup, create_app=create_app)
@click.pass_context
def run(ctx):
    click.echo("Flask app should be running now")

try:
    @my_big_cli_group.group(cls=FlaskGroup, create_app=create_app)
    def my_flask_app(ctx):
        pass
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

if __name__ == '__main__':
    try:
        my_big_cli_group()
    except Exception as e:
        print_stacktrace(e)
        exit(0)
```

This script should reproduce the issue when run with Python 3.7.3 (or any other version that reproduces the issue).