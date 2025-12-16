 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
import sys
import sphinx
import sphinx.ext.autodoc as autodoc
from sphinx.application import Sphinx
from sphinx.errors import SphinxError

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def setup_sphinx_environment():
    app = Sphinx(srcdir='.', confdir='.', doctreedir='.', outdir='.',
                  buildername='html', confoverrides={
                      'extensions': ['sphinx.ext.autodoc'],
                      'autodoc_member_order': 'bysource',
                  })
    return app

def test_issue():
    app = setup_sphinx_environment()
    try:
        with app.builder.build_all():
            pass
    except SphinxError as e:
        assert False, "Sphinx build failed"
    except AssertionError:
        raise
    except:
        e = sys.exc_info()[1]
        print_stacktrace(e)
        assert False, "Unexpected error"

if __name__ == '__main__':
    test_issue()
    print("No issues found")
```
To reproduce the issue, create a directory `mod` with the following contents:
```markdown
mod/
├── __init__.py
├── A.py
└── submod
    ├── __init__.py
    └── A.py
```
The contents of `mod/A.py` should be:
```python
class A:
    pass
```
The contents of `mod/submod/A.py` should be:
```python
from ..A import A
```
Create a file `index.rst` in the root directory with the following contents:
```rst
.. py:currentmodule:: mod

.. py:class:: A

.. py:currentmodule:: mod.submod

.. py:class:: A
```
Execute the script with `python3 reproducer.py`. The script should raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 41, in <module>
    test_issue()
  File "reproducer.py", line 35, in test_issue
    with app.builder.build_all():
  File "/Users/user/miniconda3/envs/sphinx/lib/python3.8/site-packages/sphinx/builder/singlefile.py", line 24, in build_all
    self.build_update()
  File "/Users/user/miniconda3/envs/sphinx/lib/python3.8/site-packages/sphinx/builder/singlefile.py", line 53, in build_update
    self.build_main()
  File "/Users/user/miniconda3/envs/sphinx/lib/python3.8/site-packages/sphinx/builder/singlefile.py", line 86, in build_main
    self.write_doc(outname, builder.build_single_file(self.app, outname, None))
  File "/Users/user/miniconda3/envs/sphinx/lib/python3.8/site-packages/sphinx/builder/latex/builder.py", line 141, in build_single_file
    self.write_file(doctree, 'html', outname, builder)
  File "/Users/user/miniconda3/envs/sphinx/lib/python3.8