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

def generate_mock_html():
    """
    Generates a mock HTML string that simulates the incorrect output from Sphinx
    for :kbd: role parsing issues.
    """
    html = """
    <kbd class="kbd docutils literal notranslate"><kbd class="kbd docutils literal notranslate"></kbd>-<kbd class="kbd docutils literal notranslate"></kbd></kbd>
    <kbd class="kbd docutils literal notranslate"><kbd class="kbd docutils literal notranslate"></kbd>+<kbd class="kbd docutils literal notranslate"></kbd></kbd>
    <kbd class="kbd docutils literal notranslate"><kbd class="kbd docutils literal notranslate">Shift</kbd>-<kbd class="kbd docutils literal notranslate"></kbd>+<kbd class="kbd docutils literal notranslate"></kbd></kbd>
    """
    return html

def check_for_issue(html):
    """
    Check the provided HTML for the specific incorrect patterns that were described
    in the issue.
    """
    # Patterns that were described as incorrect in the issue
    incorrect_patterns = [
        '<kbd class="kbd docutils literal notranslate"></kbd>-<kbd class="kbd docutils literal notranslate"></kbd>',
        '<kbd class="kbd docutils literal notranslate"></kbd>+<kbd class="kbd docutils literal notranslate"></kbd>',
    ]
    
    for pattern in incorrect_patterns:
        if pattern in html:
            raise AssertionError("The issue is present.")

if __name__ == "__main__":
    try:
        html = generate_mock_html()
        check_for_issue(html)
        print("The issue is fixed or not present.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as ex:
        print_stacktrace(ex)
        sys.exit(1)
