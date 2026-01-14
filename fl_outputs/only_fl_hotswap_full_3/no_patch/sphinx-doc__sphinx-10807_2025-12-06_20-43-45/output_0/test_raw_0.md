 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sphinx
import sphinx.ext.autodoc

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_automodule():
    app = sphinx.application.Sphinx(srcdir='.', confdir='.', outdir='build/html')
    app.builder = sphinx.builders.html.StandaloneHTMLBuilder(app)
    app.connect('config-inited', lambda app, config: None)
    app.connect('build-started', lambda app, excinfo: None)
    app.connect('build-finished', lambda app, excinfo: None)
    app.add_config_value('autodoc_member_order', 'bysource', 'env')
    app.add_config_value('autodoc_default_flags', ['members'], 'env')
    app.add_config_value('autodoc_mock_imports', [], 'env')
    app.add_directive('automodule', sphinx.ext.autodoc.ModuleDocumenter)
    app.add_directive('autoattribute', sphinx.ext.autodoc.AttributeDocumenter)
    app.add_directive('autoexception', sphinx.ext.autodoc.ExceptionDocumenter)
    app.add_directive('autoclass', sphinx.ext.autodoc.ClassDocumenter)
    app.add_directive('autofunction', sphinx.ext.autodoc.FunctionDocumenter)
    app.add_directive('automethod', sphinx.ext.autodoc.MethodDocumenter)
    app.add_directive('autodata', sphinx.ext.autodoc.DataDocumenter)
    app.add_directive('autoobject', sphinx.ext.autodoc.ObjectDocumenter)
    app.add_directive('autocontainer', sphinx.ext.autodoc.ContainerDocumenter)
    app.add_directive('autoenum', sphinx.ext.autodoc.EnumDocumenter)
    app.add_directive('autoevent', sphinx.ext.autodoc.EventDocumenter)
    app.add_directive('autoinstanceattribute', sphinx.ext.autodoc.InstanceAttributeDocumenter)
    app.add_directive(' Tobecovered')
    env = app.env
    env.init_env()
    settings = sphinx.environment.BuildEnvironment.get_config_value(app, 'autodoc_default_flags')
    settings.append('members')
    documenter = sphinx.ext.autodoc.ModuleDocumenter(None, None, env, 'mod')
    documenter.add_directive('function', sphinx.ext.autodoc.FunctionDocumenter)
    documenter.add_directive('submod', sphinx.ext.autodoc.ModuleDocumenter)
    documenter.add_directive('subheader', sphinx.ext.autodoc.MetaDocumenter)
    documenter.add_directive('attribute', sphinx.ext.autodoc.AttributeDocumenter)
    documenter.add_directive('constant', sphinx.ext.autodoc.DataDocumenter)
    documenter.add_directive('decorator', sphinx.ext.autodoc.DecoratorDocumenter)
    documenter.add_directive('exception', sphinx.ext.autodoc.ExceptionDocumenter)
    documenter.add_directive('class', sphinx.ext.autodoc.ClassDocumenter)
    documenter.add_directive('method