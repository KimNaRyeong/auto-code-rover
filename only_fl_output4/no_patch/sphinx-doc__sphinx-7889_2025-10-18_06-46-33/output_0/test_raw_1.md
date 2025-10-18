To address the feedback, let's refine the script to accurately replicate and diagnose the issue with the Autodoc extension's handling of generic-typed classes, ensuring it aligns with the described problem and its related environment. This refined script will attempt to invoke documentation generation on a simplified example that should trigger the described TypeError if the issue is present.

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

def generate_documentation():
    from sphinx.application import Sphinx
    import os, tempfile
    
    # Temporary directory for generating docs
    src_dir = tempfile.mkdtemp()
    with open(os.path.join(src_dir, 'conf.py'), 'w') as f:
        f.write("extensions = ['sphinx.ext.autodoc']")

    # Writing a minimal Python module with a generic class
    with open(os.path.join(src_dir, 'example.py'), 'w') as f:
        f.write("""
from typing import Generic, TypeVar

T = TypeVar('T')

class Example(Generic[T]):
    pass
""")

    build_dir = os.path.join(src_dir, '_build')
    doctree_dir = os.path.join(build_dir, 'doctrees')

    try:
        app = Sphinx(
            srcdir=src_dir,
            confdir=src_dir,
            outdir=build_dir,
            doctreedir=doctree_dir,
            buildername='html',
            freshenv=True
        )
        app.build(force_all=True)
        return True
    except Exception as e:
        print_stacktrace(e)
        return False

def main():
    assert generate_documentation(), "Failed to generate documentation."

if __name__ == "__main__":
    try:
        main()
        print("Documentation generation succeeded without errors.")
    except AssertionError as e:
        print_stacktrace(e)
        print("\nThe issue is present.")
        exit(1)
```

This script attempts to dynamically create a minimal Sphinx project in a temporary directory, incorporating a simple module that contains a generic class definition, which is the focus of this issue. If the `generate_documentation` function encounters an exception during the documentation generation process, it will invoke `print_stacktrace` to detail the error encountered. This direct approach to simulating the described environment aims to precisely trigger and diagnose the TypeError related to Autodoc's handling of generic-typed classes.