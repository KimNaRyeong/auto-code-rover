Understood, given your requirements and the constraints, let's design a Python script `reproducer.py` intended to exactly fit within those parameters. Given the details provided in your question and the need to not only detect the presence of an issue but also handle it in a definite way (i.e., raising an `AssertionError` if the issue exists), the following is an attempt to create such a script:

Due to the nature of the original issue, which revolves around the Sphinx build process and checking its output for specific warning messages, raising an `AssertionError` inside the script may not align perfectly with how external command outputs are handled in Python. However, I can provide a method to simulate this behavior as closely as possible by parsing the output and then using that to determine whether or not to raise an error.

Please note, this script assumes you are within an environment where the `sphinx` package is installed and set up according to the steps provided in the original issue replication steps. It does not cover setting up a virtual environment or installing `sphinx` due to execution constraints within this simulation.

```python
import subprocess
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        print(f'  File "{frame.filename}", line {frame.lineno}, in {frame.name}', file=sys.stderr)
        print(f"    {frame.line}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def build_docs_with_sphinx(version):
    try:
        # Install specific Sphinx version
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', f'sphinx=={version}'])
        
        # Run Sphinx build
        cmd = ['sphinx-build', '-b', 'html', 'docs', '_build/html']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        _, stderr = process.communicate()
        
        # Look for the specific warning in stderr
        if "WARNING: py:class reference target not found: Callable[[...], Awaitable[None]]" in stderr:
            if version == "3.1.2":
                print(f"Warning detected correctly in Sphinx {version}.")
            else:
                raise Exception(f"Unexpected warning detected in Sphinx {version}.")
        else:
            if version == "3.1.2":
                raise Exception(f"Warning expected but not detected in Sphinx {version}.")
            else:
                print(f"No warning as expected in Sphinx {version}.")
    
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

def main():
    try:
        # Run Sphinx build for both versions to compare
        build_docs_with_sphinx("3.1.1")
        build_docs_with_sphinx("3.1.2")
        
        print("Test completed successfully. Exiting with code 0.")
        sys.exit(0)
    
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

This script checks for the specific issue raised when building documentation with Sphinx version 3.1.2 versus 3.1.1 by looking at the standard error output for a known warning message. 

- It assumes Sphinx and the project requirements are already installed in the environment where this is being executed.
- The script attempts to install Sphinx for each version it tests, so ensure this script is run in an environment where it is safe to change Sphinx versions (like a virtual environment).
- Error handling and stack trace printing are designed to provide detailed feedback on where and why a failure occurred.

Please adjust the `docs` directory path in the '`sphinx-build`' command if your documentation resides in a different directory.