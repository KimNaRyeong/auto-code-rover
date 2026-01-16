To write a Python script (`reproducer.py`) capable of reproducing the reported Sphinx autodoc issue – where Sphinx doesn't obey the `autodoc_typehints='none'` setting for properties, resulting in type hints still being displayed in the output – we'll need a more nuanced approach. Given the challenge, the following script incorporates direct inspection of Sphinx's output on property documentation to assert the presence or absence of the issue. 

Please note, due to limitations in extracting a straightforward error message or stack trace directly from Sphinx (since it processes documentation in a batch manner rather than raising exceptions in the code flow we can catch easily for individual documentation elements), the script asserts the presence of type hints in the generated documentation and then provides guidance on verifying the issue manually if needed. 

```python
"""
reproducer.py

Attempts to programmatically reproduce the issue where Sphinx 'autodoc_typehints' set to 'none'
still shows type hints for properties in the generated documentation.
"""

import os
import subprocess
import re
import sys

def setup_sphinx_environment():
    os.makedirs("docs", exist_ok=True)
    os.makedirs("src", exist_ok=True)

    with open("src/example.py", "w") as f:
        f.write('''\
class MyClass:
    @property
    def my_property(self) -> str:
        """A simple property example."""
        return 'hello'
''')

    with open("docs/conf.py", "w") as f:
        f.write('''\
import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

project = 'Sphinx Autodoc Issue Reproducer'
extensions = ['sphinx.ext.autodoc']
html_theme = 'alabaster'
autodoc_typehints = 'none'
''')

    with open("docs/index.rst", "w") as f:
        f.write('''\
Welcome to Sphinx Autodoc Issue Reproducer's documentation!
===========================================================

.. automodule:: example
   :members:
''')

def build_docs():
    subprocess.run(["sphinx-build", "-b", "html", "docs", "docs/_build"], check=True)

def check_issue_present():
    pattern = re.compile(r'my_property.*-> str')
    with open("docs/_build/index.html", "r") as f:
        contents = f.read()
        if pattern.search(contents):
            return True
    return False

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        print(f'  File "{frame.filename}", line {frame.lineno}, in {frame.name}', file=sys.stderr)
        print(f"    {frame.line}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        setup_sphinx_environment()
        build_docs()
        issue_present = check_issue_present()
        assert not issue_present, "Issue detected: Autodoc is using type hints for properties despite 'autodoc_typehints' set to 'none'."
        print("Success: The issue is not present.")
    except Exception as e:
        print("An error occurred.", file=sys.stderr)
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**How to Use:**

1. Save this script as `reproducer.py` in the root directory of your Sphinx project (modify paths in the script if necessary to match your project structure).
2. Run the script using Python 3 (make sure Sphinx is installed): `python3 reproducer.py`
3. The script sets up a minimal Sphinx project environment, builds the documentation, and attempts to verify if the issue is present by checking the HTML output.

Please adjust the setup (module contents, configuration) as needed to better match your Sphinx project's specifics and observe the direct Sphinx output in your environment for further evidence of the issue if required.