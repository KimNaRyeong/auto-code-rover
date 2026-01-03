 Here is a standalone Python script `reproducer.py` that should reproduce the issue:
```python
def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyClass:
    @property
    def my_property(self) -> int:
        """My property docstring."""
        return 42

def test_autodoc_typehints():
    import sphinx
    import sphinx.ext.autodoc
    import tempfile
    import os

    # Create a temporary directory for the Sphinx documentation.
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a Sphinx configuration file.
        config_file = os.path.join(temp_dir, "conf.py")
        with open(config_file, "w") as f:
            f.write("""\
import sys
sys.path.insert(0, '.')

extensions = ['sphinx.ext.autodoc']
autodoc_typehints = 'none'
""")

        # Create a Sphinx documentation directory.
        doc_dir = os.path.join(temp_dir, "_build", "html")
        os.makedirs(doc_dir)

        # Create a Sphinx documentation file.
        doc_file = os.path.join(temp_dir, "index.rst")
        with open(doc_file, "w") as f:
            f.write("MyClass\n======\n\n.. autoclass:: my_module.MyClass\n   :members:\n   :undoc-members:\n   :show-inheritance:\n")

        # Create a Sphinx documentation module.
        module_file = os.path.join(temp_dir, "my_module.py")
        with open(module_file, "w") as f:
            f.write("from reproducer import MyClass\n")

        # Build the Sphinx documentation.
        app = sphinx.application.Sphinx(temp_dir, config_file)
        app.build(force_all=True, filenames=["index.html"])

        # Check that the type hint is not rendered in the output.
        with open(os.path.join(doc_dir, "index.html")) as f:
            html = f.read()
        assert "MyClass.my_property: <class 'int'>" not in html, "Type hint is rendered in the output."

if __name__ == "__main__":
    try:
        test_autodoc_typehints()
        print("No issues found.")
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
To run the script, execute the following command in the terminal:
```
python3 reproducer.py
```
If the issue is present, the script will raise an `AssertionError` and print a stack trace of the issue. If the issue is fixed, the script will print "No issues found." and exit with code 0.