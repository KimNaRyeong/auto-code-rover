Here is the reproducer script:

```python
import os
import sphinx.cmd.make_mode as make_mode
from sphinx.application import SphinxApplication

def needs_extensions(app: SphinxApplication, config):
    if app.config['needs_sphinx_gallery'] and 'sphinx_gallery' not in app.config['extensions']:
        raise ValueError(f"This project needs the extension sphinx_gallery at least in version {app.config['min_sphinx_gallery']}")

def main():
    os.chdir('doc')
    make_mode.main(['-C', '.', 'html'])
    if 'sphinx_gallery' in [ext.split('.')[-1] for ext in app.config['extensions']]:
        print("Issue reproduced. sphinx-gallery 0.10.0 should be accepted.")
    else:
        raise AssertionError("Issue not reproduced.")

if __name__ == "__main__":
    try:
        app = SphinxApplication()
        app.config['needs_sphinx_gallery'] = True
        app.config['min_sphinx_gallery'] = '0.6.0'
        needs_extensions(app, app.config)
        main()
    except Exception as e:
        print_stacktrace(e)
        raise

```

This script simulates the issue by setting up a Sphinx application with a minimum version requirement for sphinx-gallery and then tries to build the documentation. If the issue is present (i.e., sphinx_gallery 0.10.0 is not accepted), it raises an `AssertionError` and prints the stack trace.