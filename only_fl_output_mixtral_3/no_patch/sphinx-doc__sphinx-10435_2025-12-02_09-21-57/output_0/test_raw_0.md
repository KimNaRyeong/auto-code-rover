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
    app = sphinx.application.Sphinx(srcdir='.', confdir='.', outdir='.', doctreedir='.', buildername='latex', warningiserror=0)
    app.connect('builder-inited', lambda app, builder: builder.init_context(app))
    app.connect('build-finished', lambda app, exception: print_stacktrace(exception) if exception else None)
    app.setup_extension('sphinx.ext.autodoc')
    app.setup_extension('sphinx.ext.viewcode')
    app.setup_extension('sphinx.ext.doctest')
    app.setup_extension('sphinx.ext.intersphinx')
    app.setup_extension('sphinx.ext.ifconfig')
    app.setup_extension('sphinx.ext.imgmath')
    app.setup_extension('sphinx.ext.mathjax')
    app.setup_extension('sphinx.ext.ipython')
    app.setup_extension('sphinx.ext.extlinks')
    app.setup_extension('sphinx.ext.inheritance_diagram')
    app.setup_extension('sphinx.ext.napoleon')
    app.setup_extension('sphinx.ext.todo')
    app.setup_extension('sphinx.ext.coverage')
    app.setup_extension('sphinx.ext.autosummary')
    app.setup_extension('sphinx.ext.githubpages')
    app.setup_extension('sphinx.ext.jsmath')
    app.setup_extension('sphinx.ext.linkcode')
    app.setup_extension('sphinx.ext.mathbase')
    app.setup_extension('sphinx.ext.pngmath')
    app.setup_extension('sphinx.ext.sphinxapidoc')
    app.setup_extension('sphinx.ext.graphviz')
    app.setup_extension('sphinx.ext.inheritance_diagram')
    app.setup_extension('sphinx.ext.autosectionlabel')
    app.setup_extension('sphinx.ext.doctree')
    app.setup_extension('sphinx.ext.duration')
    app.setup_extension('sphinx.ext.github')
    app.setup_extension('sphinx.ext.imgconverter')
    app.setup_extension('sphinx.ext.imgscale')
    app.setup_extension('sphinx.ext.mathsingle')
    app.setup_extension('sphinx.ext.pypi')
    app.setup_extension('sphinx.ext.serializing')
    app.setup_extension('sphinx.ext.tidy')
    app.setup_extension('sphinxcontrib.bibtex')
    app.setup_extension('sphinxcontrib.blockdiag')
    app.setup_extension('sphinxcontrib.cheeseshop')
    app.setup_extension('sphinxcontrib.plantuml')
    app.setup_extension('sphinxcontrib.spelling')

    # Add custom role for inline code highlighting
    roles.register_local_role('python', highlighting.HighlightingRole())

    return