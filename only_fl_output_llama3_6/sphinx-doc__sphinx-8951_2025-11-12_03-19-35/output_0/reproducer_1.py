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

try:
    with open('docs/source/conf.py', 'w') as f:
        f.write('.. cpp:function:: std::strong_ordering operator<=>(Foo, Foo)')
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected error"

print("Issue not present. Exiting with code 0.")
exit(0)
