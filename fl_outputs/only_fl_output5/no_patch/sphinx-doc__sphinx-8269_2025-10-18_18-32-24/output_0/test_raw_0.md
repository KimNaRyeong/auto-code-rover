Sure, I'll provide a Python script named `reproducer.py` which attempts to reproduce the issue described. The script will programmatically set up a minimal Sphinx project with the linkcheck feature enabled, and then it will run the linkcheck to see if the issue (where anchor not found errors are reported instead of HTTP errors) occurs. 

```python
import subprocess
import os
from sphinx.cmd.build import main as sphinx_main

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
        # Create a new Sphinx project
        subprocess.check_call([
            'sphinx-quickstart',
            '--quiet',
            '--project', 'proj',
            '--sep',
            '--author', 'me',
            '--release', '1.0',
            '--language', 'en',
            '--no-batchfile',
            '--no-makefile',
        ])
        
        conf_py_path = os.path.join('source', 'conf.py')

        # Modify conf.py to set linkcheck_anchors = True
        with open(conf_py_path, 'a') as conf_file:
            conf_file.write("\nlinkcheck_anchors = True\n")

        # Insert a link that should return a 404
        index_rst_path = os.path.join('source', 'index.rst')
        with open(index_rst_path, 'a') as index_rst_file:
            index_rst_file.write('\n`foo <https://google.com/test.txt#test>`_\n')

    except Exception as e:
        print_stacktrace(e)
        exit(1)

def run_linkcheck():
    try:
        # Run sphinx-build linkcheck
        result = subprocess.run(['sphinx-build', '-b', 'linkcheck', '.', '_build'], text=True, capture_output=True)
        return result.stdout + result.stderr
    except Exception as e:
        print_stacktrace(e)
        exit(1)

def verify_output(output: str):
    try:
        assert "Anchor 'test' not found" not in output
        assert "404 Client Error: Not Found for url: https://google.com/test.txt" in output, "Issue exists - HTTP errors are not reported correctly."
        print("Issue fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

def main():
    setup_sphinx_project()
    output = run_linkcheck()
    verify_output(output)

if __name__ == "__main__":
    main()
```

This script works as follows:
1. It sets up a new Sphinx project using the `sphinx-quickstart` tool in silent mode with some predefined settings.
2. Modifies the `conf.py` file to set the `linkcheck_anchors` option to `True`.
3. Adds a link to the `index.rst` file, which will result in a 404 error with an anchor that doesn't exist.
4. Runs the Sphinx linkcheck (`sphinx-build` with `-b linkcheck`) and captures its output.
5. Checks if the output contains an HTTP error message instead of an anchor not found message, indicating the presence or absence of the issue.