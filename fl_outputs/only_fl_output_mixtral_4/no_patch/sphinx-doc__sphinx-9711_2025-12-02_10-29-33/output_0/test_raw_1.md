 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
import sphinx
import sphinx_gallery

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if sphinx.__version__ < '4.1.2':
    print("Sphinx version is less than 4.1.2, which is required to reproduce the issue.", file=sys.stderr)
    sys.exit(0)

if sphinx_gallery.__version__ < '0.6.0':
    print("Sphinx-gallery version is less than 0.6.0, which is required to reproduce the issue.", file=sys.stderr)
    sys.exit(0)

extensions = ['sphinx_gallery']

app = sphinx.application.Sphinx(writername='html', buildername='html', srcdir='.', confdir='.', doctreedir='.',
                                outdir='.', personalmarks=None, tags=None, verbosity=0, statusfile=None, warningiserror=0)
app.setup_extension(extensions[0])
app.connect('config-inited', lambda app, config: app.config.source_suffix = '.rst')
app.connect('config-inited', lambda app, config: app.config.extensions = extensions)
app.connect('config-inited', lambda app, config: app.config.sphinx_gallery_conf = {'backreferences_dir': 'generated'})
app.connect('config-inited', lambda app, config: app.config.html_theme = 'alabaster')
app.connect('config-inited', lambda app, config: app.config.html_static_path = ['_static'])
app.connect('config-inited', lambda app, config: app.config.html_css_files = ['custom.css'])
app.connect('config-inited', lambda app, config: app.config.html_js_files = ['custom.js'])
app.connect('config-inited', lambda app, config: app.config.release = '1.0')
app.connect('config-inited', lambda app, config: app.config.logo = '_static/mylogo.png')
app.connect('config-inited', lambda app, config: app.config.author = 'My Name')
app.connect('config-inited', lambda app, config: app.config.copyright = 'Copyright My Company')
app.connect('config-inited', lambda app, config: app.config.todo_include_todos = True)
app.connect('config-inited', lambda app, config: app.config.nitpicky = True)
app.connect('config-inited', lambda app, config: app.config.smartquotes = False)
app.connect('config-inited', lambda app, config: app.config.source_parsers = {'rst': 'recommonmark.parser'})

try:
    app.build(force_all=True, filenames=None, warningiserror=0)
except Exception as e:
    print_stacktrace(e)
    assert False, "The issue should not occur with the given versions of Sphinx and sphinx-gallery."
```
To reproduce the issue, execute the following commands in the root directory of the project:
```
$ pip install -r .doc-requirements.txt
$ pip install -e .
$ python3 reproducer.py
```
If the issue is fixed, the script should exit with code 0 without printing any error messages. If the issue is present, the script should raise an `AssertionError` and print a stack trace of the issue.