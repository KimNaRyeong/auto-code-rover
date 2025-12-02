import sympy as smp
import traceback, sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    q, u = smp.symbols(('q:2', 'u:2'), cls=smp.Function)
    assert type(q[0]) == smp.core.function.UndefinedFunction, "Symbols were created instead of Functions"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
