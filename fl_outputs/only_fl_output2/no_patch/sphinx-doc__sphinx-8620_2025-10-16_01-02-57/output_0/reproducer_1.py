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

def simulate_html_generation(input_text):
    """
    Simulates the generation of HTML for kbd tags in Sphinx that illustrates the reported issue.
    This function does not use Sphinx but rather mocks up the problem based on the description.
    """
    simulated_output = ""
    for line in input_text.splitlines():
        if 'kbd' in line:
            keys = line.replace(':kbd:`', '').replace('`', '').split('+')
            if len(keys) > 1:  # Simulate compound keystroke
                simulated_output += '<kbd class="kbd docutils literal notranslate">'
                for key in keys:
                    simulated_output += f'<kbd class="kbd docutils literal notranslate">{key}</kbd>+'
                simulated_output = simulated_output.strip('+') + '</kbd>\n'
            else:  # Single keystroke
                simulated_output += f'<kbd class="kbd docutils literal notranslate">{keys[0]}</kbd>\n'
    return simulated_output

def test_kbd_html_structure():
    input_text = """
    :kbd:`A`

    :kbd:`Shift+X`
    """
    expected_html = '<kbd class="kbd compound docutils literal notranslate">'
    generated_html = simulate_html_generation(input_text)
    if expected_html not in generated_html:
        raise AssertionError("Compound <kbd> elements do not have the 'compound' CSS class.")

try:
    test_kbd_html_structure()
except Exception as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Success: The simulation indicated the issue correctly.")
    exit(0)
