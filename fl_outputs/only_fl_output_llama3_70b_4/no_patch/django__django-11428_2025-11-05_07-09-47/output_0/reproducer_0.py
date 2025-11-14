import os
import sys
from django.apps import AppConfig
from django.utils.autoreload import raise_last_exception

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyException(Exception):
    def __init__(self, value: str, other_thing: str):
        super().__init__(value)
        self.ot = other_thing

class Config(AppConfig):
    name = "myapp"
    verbose_name = "My App"

def ready():
    raise MyException("foo", "bar")

try:
    ready()
except Exception as e:
    try:
        raise_last_exception(*sys.exc_info())
    except TypeError as te:
        print_stacktrace(te)
        assert False, "Autoreloader crashes on re-raising exceptions with custom signature"
    else:
        print("Issue is fixed")
        sys.exit(0)

sys.exit(1)
