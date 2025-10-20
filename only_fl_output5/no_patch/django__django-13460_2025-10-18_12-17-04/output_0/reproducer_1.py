# reproducer.py
def simulate_gettext_float_format_issue(value):
    """
    Simulates an issue where gettext-like formatting operations fail with float values,
    emulating the scenario with Django's blocktrans tag and float values.
    """
    try:
        # Attempting a string format with a float value in a dictionary,
        # as per the issue description.
        translated_string = "На расстоянии %(counter)s миль" % {'counter': value}
        # If the line above passes without raising an exception,
        # the issue is not reproduced.
        print("Formatted string without error:", translated_string)
        return False  # No issue detected.
    except TypeError as e:
        # Catching the TypeError, which signifies the presence of the issue.
        print_stacktrace(e)
        return True  # Issue detected.

def print_stacktrace(e: Exception):
    """
    Prints the stack trace of the exception.
    """
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

if __name__ == "__main__":
    problem_value = 1.0  # Using a float value that is expected to cause the format issue.

    issue_detected = simulate_gettext_float_format_issue(problem_value)

    assert issue_detected, "Expected to detect type error issue with float formatting but didn't."

    # If an AssertionError is not raised, then the script incorrectly believes the issue is fixed
    # This should not happen unless the formatting operation changes behavior with floats.
    print("Issue correctly detected. Exiting with code 0 because the issue is present.")
