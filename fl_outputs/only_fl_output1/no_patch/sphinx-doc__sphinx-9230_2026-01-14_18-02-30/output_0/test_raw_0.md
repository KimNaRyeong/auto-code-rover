```python
from sphinx.application import Sphinx
import os
import sys


def build_docs():
    src_dir = 'docs_source'
    conf_dir = src_dir
    out_dir = os.path.join('build', 'sphinx', 'html')
    doctree_dir = os.path.join('build', 'sphinx', 'doctrees')

    if not os.path.exists(src_dir):
        os.makedirs(src_dir)

    with open(os.path.join(src_dir, 'index.rst'), 'w') as f:
        f.write("""
Test Module
===========

.. automodule:: test_module
    :members:
    :undoc-members:
    :show-inheritance:
""")

    with open(os.path.join(src_dir, 'conf.py'), 'w') as f:
        f.write("""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
extensions = ["sphinx.ext.autodoc", "sphinx.ext.autosummary", "sphinx.ext.intersphinx", "autodocsumm"]
autosummary_generate = True
""")

    with open(os.path.join(src_dir, 'test_module.py'), 'w') as f:
        f.write('''
def sample_function(opc_meta: dict):
    """
    A sample function.

    :param dict(str, str) opc_meta: (optional)
    """
    pass
''')

    app = Sphinx(src_dir, conf_dir, out_dir, doctree_dir, 'html')
    app.build(force_all=True)

    with open(os.path.join(out_dir, 'index.html'), 'r') as f:
        content = f.read()

    if "opc_meta (dict(str,str)) – (optional)" not in content:
        raise AssertionError("Doc rendering is incorrect.")

try:
    build_docs()

except Exception as e:
    def print_stacktrace(e: Exception):
        import traceback
        import sys
        tb = traceback.extract_tb(e.__traceback__)
        print("Traceback (most recent call last):", file=sys.stderr)
        for frame in tb:
            line_number = frame.lineno
            code_context = frame.line.strip() if frame.line else "Unknown"
            print(f'  File "{frame.filename}"', file=sys.stderr)
            print(f"    {line_number}: {code_context}", file=sys.stderr)
        print(f"{e.__class__.__name__}: {e}", file=sys.stderr)
    
    print_stacktrace(e)
    sys.exit(1)

print("Documentation rendered correctly.")
sys.exit(0)
```