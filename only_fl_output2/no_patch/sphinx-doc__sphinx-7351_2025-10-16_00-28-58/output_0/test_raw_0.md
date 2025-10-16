Below is a standalone Python script that aims to reproduce the issue with Sphinx where having files with the same name but different extensions leads to unexpected behavior. The script is designed to be placed in the root directory of a sample Sphinx project, and it mimics the scenario described by running Sphinx programmatically. Upon encountering the issue, it will raise an `AssertionError` and print a detailed stack trace using the provided `print_stacktrace` function.

```python
import os
import sys
from sphinx.application import Sphinx
from sphinx.util.docutils import docutils_namespace

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# Setup minimal Sphinx environment
srcdir = '_reproducer'
if not os.path.exists(srcdir):
    os.makedirs(srcdir)

with open(os.path.join(srcdir, 'index.rst'), 'w') as f:
    f.write("""
.. toctree::
   a.md
""")

with open(os.path.join(srcdir, 'a.md'), 'w') as f:
    f.write("# Markdown File")

with open(os.path.join(srcdir, 'a.rst'), 'w') as f:
    f.write(".. _a-rst:\n\nRST File")
    
# Configuration for Sphinx
conf = {
    'extensions': ['myst_parser'],
    'master_doc': 'index',
}

# Run Sphinx
try:
    app = Sphinx(srcdir, confdir=None, outdir='_build', doctreedir='_doctree', confoverrides=conf)
    with docutils_namespace():
        app.build(force_all=True)
    built_file = os.path.join(app.outdir, 'index.html')

    # Validate the built file
    if os.path.exists(built_file):
        with open(built_file, 'r') as f:
            content = f.read()
            # Check if the Markdown file was included instead of the RST file; if not, raise assertion
            if 'Markdown File' not in content:
                raise AssertionError("The generated document does not include content from 'a.md'.")
            if 'RST File' in content:
                raise AssertionError("The generated document unexpectedly includes content from 'a.rst'.")
    else:
        raise FileNotFoundError("The 'index.html' file was not generated.")
    
    # If everything passes
    print("Success: The issue is not present.")

except (AssertionError, FileNotFoundError) as e:
    print_stacktrace(e)
    sys.exit(1)

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```

This script sets up a minimal Sphinx project with an `index.rst` that references a Markdown file (`a.md`), in the presence of an `a.rst` with the same base name but a different extension. It then builds the project and checks whether the generated HTML includes content from the Markdown file as expected. If the content from the `.rst` file is included instead or if the `.md` content is missing, an assertion is raised, triggering the stack trace output.