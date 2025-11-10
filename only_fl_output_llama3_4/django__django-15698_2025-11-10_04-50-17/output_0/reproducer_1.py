import django
from django.template import Template, Context
from django.template.base import TemplateSyntaxError
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from functools import wraps

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproducer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("Issue reproduced")
    return wrapper

@reproducer
def reproduce_issue():
    settings.configure()
    template = Template('{{ foo.count }}')
    context = Context({'foo': 'hello'})
    try:
        template.render(context)
    except Exception as e:
        raise

if __name__ == "__main__":
    reproduce_issue()
