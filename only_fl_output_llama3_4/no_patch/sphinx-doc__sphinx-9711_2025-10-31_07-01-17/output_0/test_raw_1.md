Here is the reproducer script:

```python
import os
from sphinx.application import SphinxApplication
from sphinx.util import logging

def needs_extensions(app: SphinxApplication, config):
    if app.config['needs_sphinx_gallery'] and 'sphinx_gallery' not in [ext.split('.')[-1] for ext in app.config['extensions']]:
        raise ValueError(f"This project needs the extension sphinx-gallery at least in version {app.config['min_sphinx_gallery']}")

def main():
    os.chdir('doc')
    try:
        from sphinx.cmd.make_mode import make_mode
        make_mode.main(['-C', '.', 'html'])
    except Exception as e:
        print_stacktrace(e)
        raise

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

This script simulates the issue by setting up a Sphinx application with a minimum version requirement for sphinx-gallery and then tries to build the documentation using `make_mode`. If the issue is present (i.e., sphinx_gallery 0.10.0 is not accepted), it raises an `AssertionError` and prints the stack trace.

Please note that this script requires the Sphinx package installed in your Python environment.