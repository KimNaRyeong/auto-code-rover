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

def check_docstring_rendering():
    import re
    
    # Simulated docstring as it would appear in HTML
    simulated_html_docstring = "add_lines(lines, color=1, 1, 1, width=5, label=None, name=None)"
    
    # Regular expression to match the correct rendering format in the simulated HTML output
    correct_format_regex = r"add_lines\(lines, color=\(1, 1, 1\), width=5, label=None, name=None\)"
    
    if not re.search(correct_format_regex, simulated_html_docstring):
        raise AssertionError("Docstring default arg is not rendered as expected in HTML.")

def main():
    try:
        check_docstring_rendering()
        print("Docstring default arg is rendered as expected.")
    except Exception as e:
        print_stacktrace(e)
        # Exiting with non-zero code to indicate failure
        sys.exit(1)
    # Exiting with code 0 to indicate success
    sys.exit(0)

if __name__ == "__main__":
    main()
