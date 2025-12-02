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
    app.connect('builder-inited', lambda app, builder: builder.init_theme('sphinxdoc'))
    app.connect('build-finished', lambda app, exception: print_stacktrace(exception) if exception else None)
    app.setup_extension('sphinx.ext.autodoc')
    app.setup_extension('sphinx.ext.viewcode')
    app.setup_extension('sphinx.ext.doctest')
    app.setup_extension('sphinx.ext.intersphinx')
    app.setup_extension('sphinx.ext.extlinks')
    app.setup_extension('sphinx.ext.coverage')
    app.setup_extension('sphinx.ext.mathjax')
    app.setup_extension('sphinx.ext.ifconfig')
    app.setup_extension('sphinx.ext.githubpages')
    app.setup_extension('sphinx.ext.jsmath')
    app.setup_extension('sphinx.ext.imgmath')
    app.setup_extension('sphinx.ext.latexpdf')
    app.setup_extension('sphinx.ext.linkcode')
    app.setup_extension('sphinx.ext.smartquotes')
    app.setup_extension('sphinx.ext.inheritance_diagram')
    app.setup_extension('sphinx.ext.graphviz')
    app.setup_extension('sphinx.ext.autosectionlabel')
    app.add_role('python', roles.PythonRole())
    app.connect('autodoc-process-signature', autodoc.autodoc_process_signature)
    app.connect('env-updated', lambda app, env: env.update_domain(env.app.registry. domains['python']))
    app.connect('env-updated', lambda app, env: env.domaindata['std'].pop('versionmoduledirectives', None))
    app.connect('env-updated', lambda app, env: env.domaindata['std'].pop('versionmoduleattribute', None))
    app.connect('env-updated', lambda app, env: env.domaindata['std'].pop('directive', None))
    app.connect('env-updated', lambda app, env: env.domaindata['std'].pop('default-role', None))
    app.connect('env-updated', lambda app, env: env.domaindata['std'].pop('roles', None))
    app.connect('env-updated', lambda app, env: env.domaindata['std'].pop('indices', None))
    app.connect('env-updated', lambda app, env: env.domaindata['std'].pop('initial-data', None))
    app.connect('env-updated', lambda app, env: env.domaindata['std'].pop('objects', None))
    app.connect('env-updated', lambda app, env: env.domaindata['std'].pop('objecttypes', None))
    app.connect('env-updated', lambda app, env: env.domaindata['std'].pop('tokentypes', None))
    app.connect('env-updated', lambda app, env