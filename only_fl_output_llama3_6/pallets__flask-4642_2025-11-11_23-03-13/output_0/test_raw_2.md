I apologize for the previous mistakes. Here is a new reproducer script that should reproduce the issue:

```python
import click
from flask import Flask

def create_app():
    return Flask(__name__)

@click.group()
def my_big_cli_group():
    pass

@my_big_cli_group.group(cls=FlaskGroup, create_app=create_app)
@click.pass_context
def my_flask_app(ctx):
    pass

@my_flask_app.command()
def run():
    from flask.cli import with_appcontext
    app = create_app()
    try:
        app.run()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not reproduced")

try:
    my_big_cli_group()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

if __name__ == '__main__':
    my_big_cli_group()
```

This script should reproduce the issue when you run it.