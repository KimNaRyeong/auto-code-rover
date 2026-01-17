To create a script that reproduces the issue with the spaceship operator (`<=>`) in Sphinx documentation, you'll need to simulate parsing C++ documentation with Sphinx where this operator is used. 

The following Python script aims at setting up a minimal Sphinx project, creating a simple `.rst` document that uses the problematic syntax, and then running Sphinx to build the documentation, which triggers the parsing. The script checks the Sphinx output for the specific warning/error related to the issue and raises an `AssertionError` if the issue is present. It requires Sphinx to be installed in the environment where the script is run.

Please ensure you have Sphinx installed (`pip install Sphinx`) before running this script.

```python
import subprocess
import os

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

def setup_sphinx_project():
    try:
        # Setup minimal sphinx project
        os.mkdir('test_docs')
        os.chdir('test_docs')
        os.system('sphinx-quickstart -q -p TestProject -a "Author" --ext-autodoc --makefile .')

        # Create a simple C++ file to document
        with open('test.cpp', 'w') as f:
            f.write('''
struct Foo {
    auto operator<=>(const Foo&) const = default;
};
''')

        # Create .rst file attempting to document the operator
        with open('index.rst', 'w') as f:
            f.write('''
Test Documentation
==================

.. cpp:function:: auto operator<=>(const Foo&, const Foo&)
''')
    except Exception as e:
        print_stacktrace(e)
        raise

def sphinx_build_and_check():
    try:
        # Attempt to build the documentation
        result = subprocess.run(['sphinx-build', '.', '_build'], stderr=subprocess.PIPE, text=True)

        # Check if the specific error is in the output
        if "Error when parsing function declaration" in result.stderr:
            print("Issue detected")
            print("Sphinx output:", result.stderr, sep="\n")
            raise AssertionError("Detected Sphinx parsing issue with spaceship operator")
        else:
            print("No issue detected")
            
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        setup_sphinx_project()
        sphinx_build_and_check()
    except AssertionError as e:
        print("Test failed:", e)
        exit(1)
    except Exception as e:
        print("Unexpected error:", e)
        exit(1)
    else:
        print("Test passed, issue not detected.")
        exit(0)
```

This script:
- Sets up a minimal Sphinx project in a new directory.
- Writes a simple C++ file and a corresponding `.rst` file attempting to document the spaceship operator.
- Runs `sphinx-build` to build the Sphinx documentation, capturing the stderr output.
- Checks the stderr output for the specific error message related to parsing the spaceship operator.
- Raises an `AssertionError` if the issue is detected, or prints a success message if not.