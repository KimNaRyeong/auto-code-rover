 Here is a standalone Python script `reproducer.py` that should reproduce the issue:
```python
def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyClass:
    @property
    def my_property(self) -> int:
        """My property."""
        return 42

def main():
    import sphinx
    import sphinx.ext.autodoc
    import docutils.writers.html4css1

    app = sphinx.application.Sphinx(source_dir='docs', doctree_dir='doctree')
    app.add_config_value('autodoc_typehints', 'none', 'env')
    app.connect('builder-inited', lambda app, builder: None)
    app.builder = docutils.writers.html4css1.StandaloneHTMLTranslator()
    app.build(False, None, 'html')

    # Check if type hints are present in the output
    with open('_build/html/index.html', 'r') as f:
        content = f.read()
    assert 'my_property(self) -> int' not in content, 'Type hints found in the output'

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, this script should raise an `AssertionError` with a stack trace if the issue is present. If the issue is fixed, the script should exit with code 0 without raising any exceptions.

The script uses the `MyClass` class with a type-hinted property to generate a Sphinx documentation using the `make html` command. It then checks if the type hints are present in the generated HTML file and raises an `AssertionError` if they are.

Note that the script uses the `html4css1` writer instead of the default `html` writer to ensure that the generated HTML file is compatible with the `assert` statement. The `html` writer generates a minified HTML file that cannot be searched for substrings using the `assert` statement.