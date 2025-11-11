import sys

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

try:
    import py
    assert py.__version__ == '1.1.1'
    from bin import py_bench
    py_bench.main()
except ImportError as e:
    print_stacktrace(e)
    assert False, "Issue #4840 is present"
else:
    print("Issue #4840 is fixed")
    sys.exit(0)
