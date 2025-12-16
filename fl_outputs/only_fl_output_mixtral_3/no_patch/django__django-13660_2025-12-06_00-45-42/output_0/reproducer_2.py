import sys

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

def handle(command, **options):
    """
    Reproduce the issue with exec in django/core/management/commands/shell.py.
    """
    if options['command']:
        exec(command)  # Should pass a dictionary containing a minimal set of globals.
        return

command = """
import django
def f():
    print(django.__version__)
f()
"""

try:
    handle(command)
except Exception as e:
    print_stacktrace(e)
    assert False, "Issue reproduced."

print("Issue not reproduced.")
