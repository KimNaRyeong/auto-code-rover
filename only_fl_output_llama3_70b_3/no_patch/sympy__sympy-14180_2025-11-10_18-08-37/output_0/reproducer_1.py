def latex(s):
    return "log{" + s + "}"

def test_latex_conversion():
    original_expression = "10"
    expected_latex_output = r"\ln\left(" + original_expression + r"\right)"
    actual_latex_output = latex(original_expression)
    assert actual_latex_output != "log{" + original_expression + "}", f"Expected {expected_latex_output} but got {actual_latex_output}"

def main():
    try:
        test_latex_conversion()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()

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
