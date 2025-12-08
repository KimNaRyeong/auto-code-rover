 Here is a standalone Python script `reproducer.py` that should reproduce the issue:
```python
import sphinx
import sphinx_rtd_theme

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def setup(app):
    app.add_css_file('reproducer.css')

def test():
    app = sphinx.application.Sphinx(srcdir='docs', confdir='docs', outdir='build/html')
    app.builder.build_all()
    with open('build/html/index.html') as f:
        content = f.read()
    assert 'created_at: datetime' not in content, 'Type hints found in output'

if __name__ == '__main__':
    try:
        test()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    else:
        print('No type hints found in output')
        exit(0)
```
This script sets up a Sphinx application with the `sphinx_rtd_theme` theme, adds a custom CSS file to remove the type hints, and defines a `test` function that builds the HTML documentation and checks for the presence of type hints in the generated `index.html` file.

To use this script, create a new file `reproducer.css` in the `docs` directory with the following content:
```css
.rst-content .type {
    display: none;
}
```
This CSS rule hides the type hints in the generated HTML.

Then, run the script with `python3 reproducer.py`. If the issue is present, the script will print a stack trace and exit with code 1. If the issue is fixed, the script will print a success message and exit with code 0.