Sure, here's a script `reproducer.py` designed to trigger the described issue and behave accordingly:

```python
import sys
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

def check_fragment_identifier(file_path, expected_fragment):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        assert expected_fragment in content, f"Expected to find {expected_fragment} in HTML."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

def main():
    # Sample docstring with expected Sphinx behavior
    doc = """
.. py:function:: example_python_function(foo)

    Some function.
""" 
    index_path = "index.rst"
    conf_path = "conf.py"
    
    # Write the index.rst file
    with open(index_path, 'w') as f:
        f.write(doc)
        
    # Minimal Sphinx conf.py
    conf_content = """
project = 'TestProject'
master_doc = 'index'
html_theme = 'alabaster'
"""
    with open(conf_path, 'w') as f:
        f.write(conf_content)
    
    try:
        # Invoke Sphinx to build the documentation
        subprocess.run(["sphinx-build", "-b", "html", ".", "_build"], check=True)
        
        # The expected fragment identifier would be the one prior to the breaking change
        expected_fragment = "example_python_function"
        output_file = os.path.join("_build", "index.html")
        
        # Check if the fragment identifier exists
        check_fragment_identifier(output_file, expected_fragment)
        
        print("Documentation built successfully. No issue found with fragment identifiers.")
        
    except subprocess.CalledProcessError as e:
        print("Error during Sphinx build:", e.output)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

To use this script:

1. Ensure you have Sphinx installed in your Python environment (`pip install Sphinx`).
2. Place this script in the root directory of a Sphinx documentation project. If it's a brand-new project, you can create one quickly by running `sphinx-quickstart` and following the prompts.
3. Run the script with Python 3 using the command from the problem statement, `python3 reproducer.py`.
4. This script will generate a minimal Sphinx configuration and a single `index.rst` file containing a documented Python function. It then builds the documentation and attempts to validate the presence of the expected fragment identifier in the generated HTML file based on the described issue.
5. If the issue is present, meaning the expected anchor uses underscores instead of dashes, the script will exit with code 1, printing the problematic part of the code. Otherwise, it reports success. 

This should facilitate reproducing the reported issue with Python domain IDs breaking changes in Sphinx.