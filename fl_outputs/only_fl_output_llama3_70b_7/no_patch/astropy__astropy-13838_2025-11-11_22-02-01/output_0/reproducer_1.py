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

def main():
    try:
        # Put the code that reproduces the issue here
        # For example, if the issue is with a specific function or module
        from non_existent_module import non_existent_function
        non_existent_function()
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue reproduced"

if __name__ == "__main__":
    main()
