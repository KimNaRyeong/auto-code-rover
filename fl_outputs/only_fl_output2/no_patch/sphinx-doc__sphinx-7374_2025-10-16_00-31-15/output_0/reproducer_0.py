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

def generate_fragment_identifier(function_name: str) -> str:
    """
    Mock function to mimic the Sphinx behavior for generating fragment
    identifiers for Python functions. This is where the issue is reproduced.
    """
    # The behavior being tested for reproduction: replacing underscores with dashes.
    # This should represent the change that caused the issue.
    fragment_identifier = function_name.replace('_', '-')
    return fragment_identifier

def main():
    test_function_name = 'example_python_function'
    expected_fragment = 'example_python_function'  # This is the expected behavior before the breaking change
    generated_fragment = generate_fragment_identifier(test_function_name)

    try:
        # Asserting the generated fragment identifier matches the expected (original) format.
        assert generated_fragment == expected_fragment, f"Fragment identifier changed from underscores to dashes: expected {expected_fragment}, got {generated_fragment}"
    except AssertionError as e:
        print_stacktrace(e)
        raise e  # Re-raise the exception after printing the stack trace

    print("Issue not present. Fragment identifier matches expected format.")

if __name__ == "__main__":
    try:
        main()
    except AssertionError:
        exit(1)
    else:
        exit(0)
