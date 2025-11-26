import os
import sys
from django.utils.autoreload import raise_last_exception
from django.apps import AppConfig

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

    def ready(self):
        raise MyException("foo", "bar")

try:
    config = Config()
    try:
        config.ready()
    except Exception as e:
        original_exception = e
    raise_last_exception(original_exception)
except TypeError as te:
    print_stacktrace(te)
    assert False, "Autoreloader crashes on re-raising exceptions with custom signature"
else:
    sys.exit(0)

sys.exit(1)
