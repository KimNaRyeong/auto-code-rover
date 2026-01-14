 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sphinx
import sphinx.ext.autodoc as autodoc
import sphinx.writers.latex as latex
import sphinx.roles as roles
import sphinx.highlighting as highlighting

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def setup():
    app = sphinx.application.Sphinx(srcdir='.', confdir='.',
                                     outdir='build/html', doctreedir='build/doctree',
                                     buildername='html', confoverrides={})
    app.add_config_value('highlight_language', 'python3', False)
    app.connect('builder-inited', lambda app, builder: builder.init_highlighting())
    app.setup_extension(autodoc)
    app.setup_extension(latex)
    app.setup_extension(roles)
    app.setup_extension(highlighting)
    app.add_role('python', highlighting.PythonRole())
    return app

def test():
    app = setup()
    app.build(['index.rst'], ['latexpdf'])
    with open('build/latex/index.tex', 'r') as f:
        content = f.read()
    expected = 'Inlined code: \\texttt{def foo(1 + 2 + None + "abc"): pass}'
    assert expected in content, 'Unexpected output in build/latex/index.tex'

if __name__ == '__main__':
    try:
        test()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
The script sets up a minimal Sphinx application, adds the necessary extensions, and builds the `index.rst` file using the `latexpdf` builder. It then checks the generated `build/latex/index.tex` file for the presence of the inlined code with a space character at the beginning and end.

To run the script, create a new directory, place the `reproducer.py` file in it, and run `python3 reproducer.py`. If the issue is present, the script will print a stack trace and raise an `AssertionError`. If the issue is fixed, the script will exit with code 0.

Note: The `index.rst` file used in the script should contain the following content:
```rst
.. role:: python(code)
   :language: python
   :class: highlight

Inline :python:`def foo(1 + 2 + None + "abc"): pass` code block

.. code-block:: python

   def foo(1 + 2 + None + "abc"): pass
```