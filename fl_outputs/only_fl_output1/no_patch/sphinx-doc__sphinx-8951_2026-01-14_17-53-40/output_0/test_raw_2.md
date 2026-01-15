Given the context, we'll design a Python script named `reproducer.py` that aims to programmatically generate a minimal Sphinx project, attempts to document a C++ function using the spaceship operator, and checks for the described Sphinx parsing issue. The script will raise an `AssertionError` if the issue is detected or complete successfully otherwise. We make use of Sphinx's API to simulate the documentation generation process.

```python
import os
from sphinx.application import Sphinx
import sys

def setup_sphinx_project():
    """
    Set up a minimal Sphinx project with a single .rst file
    that includes the C++ function using the spaceship operator.
    """
    if not os.path.exists('test_project/docs'):
        os.makedirs('test_project/docs')

    with open('test_project/docs/conf.py', 'w') as f:
        f.write("project = 'Test Project'\n")
        f.write("extensions = ['sphinx.ext.intersphinx']\n")

    with open('test_project/docs/index.rst', 'w') as f:
        f.write(".. cpp:function:: auto operator<=>(const Foo&, const Foo&) -> std::strong_ordering\n")

def run_sphinx():
    """
    Run Sphinx to build the documentation, and check for errors.
    """
    app = Sphinx(
        srcdir='test_project/docs',
        confdir='test_project/docs',
        outdir='test_project/docs/_build',
        doctreedir='test_project/docs/_doctrees',
        buildername='html',
        warningiserror=True  # Treat warnings as errors
    )
    app.build(force_all=True)
    return app.statuscode

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

def main():
    setup_sphinx_project()
    try:
        status_code = run_sphinx()
        if status_code != 0:
            raise AssertionError("Sphinx failed to handle the C++ spaceship operator correctly.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("An unexpected error occurred during Sphinx project build.")

    print("Sphinx successfully parsed the C++ spaceship operator. The issue is fixed.")

if __name__ == '__main__':
    try:
        main()
    except AssertionError as error:
        sys.exit(1)
    else:
        sys.exit(0)
```

Instructions and details:

1. This script creates a small Sphinx project in the `test_project/docs` directory, which includes a configuration file (`conf.py`) and a single source file (`index.rst`). The source file attempts to document a C++ function that utilizes the spaceship operator `<=>`.
2. The script then runs Sphinx to build the HTML documentation. We treat warnings as errors (`warningiserror=True`) to ensure we catch any related warnings during the build.
3. If Sphinx encounters an error or warning related to the parsing of the function declaration, the script will capture this as a failure state, invoke the `print_stacktrace` function to provide error details, and raise an `AssertionError`.
4. If the documentation builds successfully without warnings/errors related to the spaceship operator, it means Sphinx has likely resolved the issue, and the script exits with code 0 to indicate success.
5. Before running this script, ensure Sphinx is installed in your Python environment (`pip install sphinx`).

Please note that the functionality and error handling of this script are based on the described scenario and assumptions. Adjustments may be necessary for different Sphinx configurations or setups.