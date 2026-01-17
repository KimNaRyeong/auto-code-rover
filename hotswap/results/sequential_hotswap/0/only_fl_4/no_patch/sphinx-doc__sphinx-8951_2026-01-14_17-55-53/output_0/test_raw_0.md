Here is a standalone Python script named `reproducer.py` designed to reproduce the issue with the Sphinx parsing error related to the C++20 spaceship operator (`<=>`). This script automates the Sphinx documentation building process for a minimal example that triggers the mentioned error. It will check for the presence of the error in Sphinx's output and raise an `AssertionError` if the issue is detected or exit with code 0 if the issue is fixed.

```python
import subprocess
import os
import sys

# Function to print stack trace of the exception
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

def check_sphinx_output(output: str):
    error_message = "Invalid C++ declaration: Expecting \"(\" in parameters-and-qualifiers"
    if error_message in output:
        raise AssertionError("Sphinx failed to parse the spaceship operator as expected.")

def setup_sphinx_environment():
    doc_directory = "docs"
    os.makedirs(doc_directory, exist_ok=True)
    
    conf_py_content = """
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

project = 'TestProject'
extensions = []
master_doc = 'index'
html_theme = 'alabaster'
    """

    index_rst_content = """
Welcome to TestProject's documentation!
========================================

.. toctree::
   :maxdepth: 2

.. cpp:function:: std::strong_ordering operator<=>(Foo, Foo)
    """

    with open(os.path.join(doc_directory, 'conf.py'), 'w') as fp:
        fp.write(conf_py_content)

    with open(os.path.join(doc_directory, 'index.rst'), 'w') as fp:
        fp.write(index_rst_content)

def build_sphinx_docs():
    result = subprocess.run(["sphinx-build", "-b", "html", "docs", "build"], capture_output=True, text=True)
    return result.stdout + "\n" + result.stderr

def main():
    setup_sphinx_environment()
    try:
        output = build_sphinx_docs()
        check_sphinx_output(output)
        print("No issue detected. The spaceship operator is supported correctly by Sphinx.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
```

To use this script:

1. Place this script in the root directory of your Sphinx project.
2. Ensure you have Sphinx installed (`pip install sphinx`) in your Python environment.
3. Execute the script using Python 3 (`python3 reproducer.py`).

The script will:

- Create a minimal Sphinx environment and configuration.
- Generate an `index.rst` file containing the example that should trigger the parsing issue with the spaceship operator.
- Build the Sphinx documentation, capturing the output.
- Check the output for the specific error message related to the spaceship operator.
- Raise an `AssertionError` if the error is present (indicating the issue is reproducible) or exit with code 0 if the issue is not detected (indicating the issue may be fixed or the conditions have changed).