# reproducer.py
import inspect
import sys

DEFAULT_OPTION = 'default'

def do_something(msg, option=DEFAULT_OPTION):
    """A function that does something."""
    print(msg)

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

def emulate_sphinx_autodoc():
    func = do_something
    sig = inspect.signature(func)
    parameters = sig.parameters

    # This is a naive emulation and not how Sphinx's autodoc actually operates.
    # Sphinx uses more sophisticated means to document APIs, including handling of constants.
    documented_signature = f"{func.__name__}("
    documented_params = []
    for name, param in parameters.items():
        if param.default is not param.empty:
            # This simplified check replaces constant with its value.
            # Sphinx's behavior might differ especially in how it records or represents default values in documentation.
            documented_params.append(f"{name}={param.default!r}")
        else:
            documented_params.append(name)
    documented_signature += ", ".join(documented_params) + ")"
    return documented_signature

try:
    expected = "do_something(msg, option=DEFAULT_OPTION)"
    result = emulate_sphinx_autodoc()
    assert result == expected, f"Expected: {expected}, but got: {result}"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    print("The issue is fixed. No replacement of constants with their values in the documentation signature.")
    sys.exit(0)
