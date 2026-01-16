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

def test_kbd_role_issue():
    from docutils.core import publish_parts
    from docutils.writers.html4css1 import Writer

    # Define the problematic kbd roles
    problematic_roles = [
        ':kbd:`-`',
        ':kbd:`+`',
        ':kbd:`Shift-+`'
    ]

    # The expected correct behavior
    expected_outputs = [
        '<kbd class="kbd docutils literal notranslate">-</kbd>',
        '<kbd class="kbd docutils literal notranslate">+</kbd>',
        '<kbd class="kbd docutils literal notranslate"><kbd class="kbd docutils literal notranslate">Shift</kbd>+<kbd class="kbd docutils literal notranslate">+</kbd></kbd>'
    ]

    # Checking each kbd role against its expected output
    for role, expected in zip(problematic_roles, expected_outputs):
        # HTML transformation
        output = publish_parts(role, writer=Writer())['html_body']
        if expected not in output:
            # If not matching, raise an AssertionError
            raise AssertionError(f'Output for {role} did not match expected output.\nExpected: {expected}\nGot: {output}')

try:
    test_kbd_role_issue()
    print("Test passed: No issues found.")
except AssertionError as e:
    print_stacktrace(e)
    raise SystemExit(1)
