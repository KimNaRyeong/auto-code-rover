```python
# reproducer.py

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

def main():
    import os
    import subprocess
    import tempfile

    # Prepare Sphinx environment
    try:
        temp_dir = tempfile.mkdtemp()
        test_file = os.path.join(temp_dir, 'test.rst')
        conf_file = os.path.join(temp_dir, 'conf.py')

        # Create a minimal Sphinx conf.py
        with open(conf_file, 'w') as f:
            f.write("project = 'TestProject'\n")
            f.write("extensions = ['sphinx.ext.autodoc']\n")

        # Create an RST file containing a Python function with underscores
        with open(test_file, 'w') as f:
            f.write('.. py:function:: example_python_function(foo)\n\n')
            f.write('   Some function.\n')

        # Run Sphinx to build HTML
        build_dir = os.path.join(temp_dir, '_build')
        cmd = ['sphinx-build', '-b', 'html', temp_dir, build_dir]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Verify the generated HTML has the expected fragment identifier
        with open(os.path.join(build_dir, 'index.html'), 'r') as f:
            content = f.read()
            expected_fragment = 'example_python_function'
            if f'href="#{expected_fragment}"' not in content:
                raise AssertionError(f"Fragment identifier '{expected_fragment}' not found.")

        print("No issue detected.")

    except Exception as e:
        print_stacktrace(e)
        exit(1)
    
    finally:
        # Optionally: Clean up the temporary directory if needed
        pass

if __name__ == "__main__":
    main()
```

This script sets up a minimal Sphinx project in a temporary directory, including a single `.rst` file that documents a Python function with underscores in its name. It then runs `sphinx-build` to generate HTML documentation for this project. After building, it checks the resulting `index.html` for a link with the expected fragment identifier using underscores. If the expected identifier uses dashes instead (indicating the issue is present), an `AssertionError` is raised, and the script prints a stack trace. The script exits with code 0 if the issue is fixed, meaning it cannot find the problematic dash-separated identifier and instead finds the correct underscore-separated identifier.