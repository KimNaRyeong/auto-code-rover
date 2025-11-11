Here is the reproducer script:

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

@my_big_cli_group.group(cls=AppGroup, create_app=create_app)
@click.pass_context
def my_flask_app(ctx):
    pass

@my_flask_app.command()
@click.pass_context
def run(ctx):
    click.echo("Running Flask app")

if __name__ == '__main__':
    try:
        my_big_cli_group()
        my_flask_app.run()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected NoAppException but got another exception")
```

This script should be run with `python3 reproducer.py`.