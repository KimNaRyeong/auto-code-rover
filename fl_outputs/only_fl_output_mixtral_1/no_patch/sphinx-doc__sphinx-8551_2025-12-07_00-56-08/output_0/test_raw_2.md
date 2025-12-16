 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import sphinx
import sphinx_rtd_theme

def setup(app):
    app.add_css_file('css/theme-overrides.css')
    app.connect('config-inited', configure)

def configure(app, config):
    config.html_theme = 'sphinx_rtd_theme'
    config.html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == '__main__':
    try:
        app = sphinx.application.Sphinx(srcdir='.', confdir='.', outdir='.', doctreedir='.', buildername='html', confoverrides={
            'source_suffix': '.rst',
            'master_doc': 'index',
            'html_theme': 'alabaster',
            'numfig': True,
            'pygments_style': 'sphinx',
            'html_static_path': ['_static'],
            'html_sidebars': {
                '**': [
                    'globaltoc.html',
                    'searchbox.html',
                    'sourcelink.html',
                    'navigation.html',
                    'relations.html',
                    'footer.html'
                ]
            }
        })
        app.connect('config-inited', setup)
        app.build(force_all=True)
    except Exception as e:
        print_stacktrace(e)
        raise
```
To reproduce the issue, create a directory structure as follows:
```diff
- reproducer.py
- _static/
  - css/
    - theme-overrides.css
- mod/
  - __init__.py
  - A.py
- mod/submod/
  - __init__.py
  - A.py
- index.rst
```
The contents of the files are as follows:

`mod/__init__.py`:
```python
from .A import A as _A
```
`mod/A.py`:
```python
class A:
    pass
```
`mod/submod/__init__.py`:
```python
from .A import A as _A
```
`mod/submod/A.py`:
```python
class A:
    pass
```
`index.rst`:
```rst
.. py:currentmodule:: mod

.. py:class:: A

.. py:currentmodule:: mod.submod

.. py:class:: A

.. py:currentmodule:: mod

.. py:function:: f

   - :py:class:`A`
   - :py:class:`mod.A`
   - :py:class:`mod.submod.A`

   :param A a:
   :param mod.A b:
   :param mod.submod.A c:
   :rtype: A
   :rtype: mod.A
   :rtype: mod.submod.A

.. py:currentmodule:: mod.submod

.. py:function:: f

   - :py:class:`A`
   - :py:class:`mod.A`
   - :py:class:`mod.submod.A`

   :param A a: BUG: links to mod.A instead of mod.submod.A
   :param mod.A b:
   :param mod.submod.A c:
   :rtype: A
   :r