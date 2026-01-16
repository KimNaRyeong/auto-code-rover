Certainly! Below is a `reproducer.py` Python script made to demonstrate the specified issue regarding `urlize()` function handling. Execute this script at the root level of your project. It is intended to catch the problem, raise an `AssertionError` if the issue exists, and report a detailed stack trace for easier debugging.

```python
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

def urlize(text: str) -> str:
    # This is a simplistic placeholder function.
    # Replace this with your actual urlize function implementation
    # that you intend to test.
    return text

def test_urlize_with_html_escaped_string_and_trailing_punctuation():
    input_text = 'Search for google.com/?q=1&lt! and see.'
    expected = 'Search for <a href="http://google.com/?q=1%3C">google.com/?q=1&lt</a>! and see.'
    try:
        output = urlize(input_text)
        assert output == expected, f"Output did not match expected. Got: {output}, Expected: {expected}"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1) # Exit with non-zero to indicate failure
    except Exception as e:
        print_stacktrace(e)
        exit(1) # Handle other exceptions as failure scenarios
    print("No issues detected, test passed.")
    exit(0)

if __name__ == "__main__":
    test_urlize_with_html_escaped_string_and_trailing_punctuation()
```

Follow the steps to adapt this script correctly:

1. **Implement or Import `urlize` Function**: The placeholder `urlize` function in this script should be replaced or modified to test the actual `urlize` function in your project. If the real `urlize` function is part of a module, you should import it at the beginning of this script.

2. **Run the Test**: Place this script at the root of your project directory. Run the script using `python3 reproducer.py`. 

3. **Interpret Output**: If the script prints "No issues detected, test passed." and exits with code 0, your `urlize` function does not have the reported issue. However, if it prints a stack trace and exits with code 1, the issue is present as described.

This script serves both as an immediate validation tool and as a starting point for setting up automated testing frameworks in the future.