# reproducer.py

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
        from django.utils.dateparse import parse_time
        # Test cases that arguably should not pass but do due to the current regex.
        test_cases = ['0:5: ', '25:00', '12:60']  # Example cases based on 'loose' regex definitions.
        for case in test_cases:
            result = parse_time(case)
            if result is not None:
                raise AssertionError(f"Invalid time string '{case}' should not be parsed.")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
