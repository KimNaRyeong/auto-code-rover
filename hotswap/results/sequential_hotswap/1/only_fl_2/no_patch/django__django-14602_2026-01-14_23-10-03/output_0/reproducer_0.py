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

def test_parse_time_with_invalid_options():
    # The issue is related to the Django's utility function for parsing times.
    # The purpose of this test case is to reproduce the issue by providing 
    # an input string that includes technically invalid time formats and 
    # asserting that the function should not accept these formats.
    # Ideally, such inputs should either throw an exception or return None,
    # depending on how the `parse_time` function will be adjusted to handle 
    # the invalid inputs.

    from django.utils.dateparse import parse_time
    from datetime import time

    invalid_time_inputs = [
        "0:5: ",  # Trailing space
        "25:00",  # Hour out of valid range
        "0:60",   # Minute out of valid range
        "::",     # All values missing
        "24:01",  # Invalid hour value (24 is only valid if minutes and seconds are 0)
    ]

    for input_str in invalid_time_inputs:
        try:
            result = parse_time(input_str)
            assert result is None, f"Expected None for invalid input '{input_str}', got {result}"
        except Exception as e:
            print(f"Failed on input: '{input_str}'")
            print_stacktrace(e)
            raise

    # If no AssertionErrors were raised till now, then all invalid inputs are considered
    # correctly handled (either by raising exceptions or returning None).
    print("All invalid inputs were correctly not accepted.")

try:
    test_parse_time_with_invalid_options()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
