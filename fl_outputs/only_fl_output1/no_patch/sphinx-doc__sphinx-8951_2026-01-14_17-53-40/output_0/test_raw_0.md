Here's a standalone Python script named `reproducer.py` that aims to reproduce the issue with Sphinx not supporting C++20's spaceship operator in its documentation. This script dynamically generates a minimal Sphinx project, attempts to document a C++ function using the spaceship operator, and verifies if the build outputs an error related to this operator.

```python
import os
import subprocess
import sys

def create_sphinx_project():
    os.makedirs('test_docs', exist_ok=True)
    with open('test_docs/conf.py', 'w') as f:
        f.write("project = 'Test Documentation'\n")
        f.write("extensions = ['breathe']\n")
        f.write("breathe_projects = { 'test': './xml' }\n")
        f.write("breathe_default_project = 'test'\n")
    with open('test_docs/index.rst', 'w') as f:
        f.write('.. toctree::\n\n')
        f.write('.. cpp:function:: std::strong_ordering operator<=>(Foo, Foo)\n')


def generate_doxygen_xml():
    os.makedirs('xml', exist_ok=True)
    with open('Doxyfile', 'w') as f:
        f.write('GENERATE_XML = YES\n')
        f.write('XML_OUTPUT = xml\n')
        f.write('INPUT = .\n')
    subprocess.run(['doxygen', 'Doxyfile'], check=True)


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


def run_sphinx():
    try:
        subprocess.run(['sphinx-build', '-b', 'html', 'test_docs', 'test_docs/_build'],
                       check=True, text=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        sys.exit(1)


def verify_issue():
    output = subprocess.run(['sphinx-build', '-M', 'html', 'test_docs', 'test_docs/_build', '-q'],
                            capture_output=True, text=True)
    error_message = "Error in declarator or parameters-and-qualifiers"
    if error_message in output.stderr:
        raise AssertionError("Sphinx C++20 spaceship operator issue is present.")
    else:
        print("No issues detected with the spaceship operator. Exiting with code 0.")


def main():
    print("Setting up Sphinx project...")
    create_sphinx_project()
    print("Generating Doxygen XML...")
    generate_doxygen_xml()
    print("Running Sphinx...")
    run_sphinx()
    print("Verifying the issue...")
    try:
        verify_issue()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()
```

This script includes the following steps:
1. Creates a minimal Sphinx project with a configuration that presumes the "Breathe" extension is used to integrate Doxygen documentation into Sphinx docs.
2. Generates Doxygen documentation (assuming that the environment has Doxygen installed and there's some source available to document; this script does not generate any C++ source).
3. Runs Sphinx to build the documentation.
4. Verifies if the build generated a specific error related to the spaceship operator.

**Note**: For this script to function:
- You need Python 3.x installed.
- Ensure Sphinx and Breathe are installed in your environment. You can install them using pip (`pip install Sphinx breathe`).
- Doxygen must be installed and accessible from the command line.
- This script assumes that an error specifically related to parsing the spaceship operator will occur and be present in the build's stderr.
- If the project structure or the manner in which Sphinx or Breathe reports errors changes, the script may need an update.
- The script may need adjustments for Windows, especially around subprocess invocation.

**Important Consideration**: Since this script attempts to run Sphinx and expects specific behavior, the actual issue reproduction might hinge critically on the version of Sphinx, Breathe, and Doxygen used, as well as the specific project configuration and setup.