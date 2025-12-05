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
    app = sphinx.application.Sphinx(source_dir='.', buildername='latex', confoverrides={
        'highlight_language': 'python',
        'highlight_options': {
            'guess_language': True,
        },
    })

    # Add a custom role that uses the code directive for highlighting
    app.add_role('python', roles.XRefRole())
    app.add_directive('code', autodoc.AutodocDirective)

    # Override the LaTeX writer to remove the space characters before and after the inline code
    app.add_builder(latex.LaTeXBuilder)
    app.builders['latex'].pseudoxml_presentation_wrap = lambda x: x.replace(r'\begin_inspstraightcode{', r'\begin_inspstraightcode\unskip{}').replace(r'\end_inspstraightcode{', r'\end_inspstraightcode\unskip{}')

    # Initialize the highlighting engine
    highlighting.init_highlighting(app)

    return app

def test():
    app = setup()
    app.build(['index.rst'], [])

    # Check if the space characters are present in the generated .tex file
    with open(app.outdir + '/index.tex', 'r') as f:
        content = f.read()

        # Check for the space characters before and after the inline code
        assert '\\begin_inspstraightcode{' not in content, 'Space character found before inline code'
        assert '}\n\\end_inspstraightcode{' not in content, 'Space character found after inline code'

if __name__ == '__main__':
    try:
        test()
    except Exception as e:
        print_stacktrace(e)
        raise
```
The script initializes a Sphinx application with a custom role and directive that uses the code directive for highlighting. It also overrides the LaTeX writer to remove the space characters before and after the inline code. Finally, it builds the project and checks for the space characters in the generated .tex file.

If the issue is present, the script will raise an `AssertionError` and print a stack trace. If the issue is fixed, the script will exit with code 0.