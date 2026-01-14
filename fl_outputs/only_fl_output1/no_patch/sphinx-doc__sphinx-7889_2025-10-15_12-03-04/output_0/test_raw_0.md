Here's a potential `reproducer.py` script tailored to simulate the environment and trigger the described issue with Sphinx's Autodoc extension when handling generic-typed classes. This script assumes that the necessary packages (`sphinx`, `pyhamcrest`, `selenium`, `typing_extensions`) are already installed in the environment where it is being executed.

```python
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

def simulate_sphinx_build():
    from sphinx.application import Sphinx
    import os

    # Setup dummy Sphinx project directory
    src_dir = os.path.abspath("temp_docs_src")
    conf_dir = src_dir
    out_dir = os.path.abspath("temp_docs_build")
    doctree_dir = os.path.abspath("temp_doctrees")
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(doctree_dir, exist_ok=True)

    # Minimal Sphinx config to trigger the autodoc extension
    with open(os.path.join(src_dir, 'conf.py'), 'w') as conf_file:
        conf_file.write("""
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
extensions = [
    'sphinx.ext.autodoc',
]
""")

    # Dummy module with a generic-typed class to document
    with open(os.path.join(src_dir, 'example_module.py'), 'w') as example_module:
        example_module.write("""
from typing import Generic, TypeVar

T = TypeVar('T')

class ExampleClass(Generic[T]):
    pass
""")

    # Dummy index file to include the problematic module
    with open(os.path.join(src_dir, 'index.rst'), 'w') as index_file:
        index_file.write("""
Welcome to the Test documentation!
===================================

.. automodule:: example_module
   :members:
   :undoc-members:
   :show-inheritance:
""")

    return Sphinx(
        srcdir=src_dir,
        confdir=conf_dir,
        outdir=out_dir,
        doctreedir=doctree_dir,
        buildername='html'
    )


def main():
    try:
        app = simulate_sphinx_build()
        app.build()
        print("Documentation built successfully. Issue seems fixed.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.") from e

    # Clean-up logic can go here if necessary

if __name__ == "__main__":
    main()
```

### Notes:
- This script sets up a minimal Sphinx environment programmatically within the same Python script, so it sidesteps the need for a separate Sphinx project.
- The `simulate_sphinx_build()` function creates a temporary Sphinx project with a single file module `example_module.py` containing a generic-typed class, which is intended to reproduce the `TypeError` described in the issue when Sphinx's autodoc tries to document it.
- The script concludes with an `AssertionError` when it encounters the specified issue, which means it could serve well for both reproducing the problem and as part of an automated test suite to verify whether the issue gets resolved after changes to the autodoc extension or its dependencies.