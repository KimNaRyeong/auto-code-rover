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

def check_kbd_output(html: str, expected_classes: list[str]):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    kbd_elements = soup.find_all('kbd')
    for kbd, expected_class in zip(kbd_elements, expected_classes):
        classes = kbd.get('class', [])
        assert expected_class in classes, f"Expected '{expected_class}' class in <kbd> element attributes {classes}"

def generate_html():
    from docutils.core import publish_string
    docutils_settings = {'syntax_highlight': 'none'}
    rst_source = """
:kbd:`A`

:kbd:`Shift+X`
"""
    html = publish_string(source=rst_source, writer_name='html', settings_overrides=docutils_settings)
    return html.decode('utf-8')

def main():
    html = generate_html()
    try:
        check_kbd_output(html, ['literal', 'compound'])
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    print("Issue not present, exiting with code 0.")
    exit(0)

if __name__ == "__main__":
    main()
```

This script attempts to reproduce the issue as documented:

- It generates HTML from reStructuredText (RST) content that includes `:kbd:` role usage.
- It then checks if the generated `<kbd>` HTML elements have the desired CSS classes to differentiate between single and compound keystrokes.
- The `check_kbd_output` function looks for expected classes in the class attribute of `<kbd>` tags parsed by BeautifulSoup.
- When the expectations are not met, it raises an `AssertionError`, triggering the `print_stacktrace` function to display where the issue occurred.
- If the script exits with code 0, it indicates that the issue has been fixed or is not present.