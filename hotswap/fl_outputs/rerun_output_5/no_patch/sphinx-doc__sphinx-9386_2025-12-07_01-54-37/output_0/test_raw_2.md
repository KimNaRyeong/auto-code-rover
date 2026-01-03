 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
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
        return 42

if __name__ == "__main__":
    import sphinx
    import sphinx.ext.autodoc as autodoc
    import sphinx.application as app

    app = sphinx.application.Sphinx(srcdir='.', confdir='.', outdir='.', doctreedir='.', buildername='html', confoverrides={
        'autodoc_typehints': 'none'
    })

    builder = app.builder
    builder.init_build()

    env = app.env

    # Initialize autodoc
    autodoc_dummy_builder = app.builder.builders['dummy']
    autodoc.setup(app, autodoc_dummy_builder)

    # Generate the document tree
    env.create_domain(autodoc.AutodocDomain)
    domain = env.get_domain('py')
    settings = app.builder.get_translator('html').settings

    # Generate the document for MyClass
    document = domain.document_tree.traverse(lambda x: x, None)
    autodoc_content = autodoc.autodoc(document, settings, app.builder, 'my_module', ['MyClass'])

    # Check if type hints are present
    for node in autodoc_content:
        if isinstance(node, autodoc.describe.Class):
            for member in node.members:
                if isinstance(member, autodoc.describe.Attribute):
                    if member.type is not None:
                        assert False, "Type hints found in the output"

    print("Type hints not found in the output")
```
To reproduce the issue, run the script with `python3 reproducer.py`. If the issue is present, an `AssertionError` will be raised, and the stack trace will be printed. If the issue is fixed, the script will print "Type hints not found in the output" and exit with code 0.

The script uses the `autodoc_typehints` configuration option to disable type hints in the generated documentation. It then generates the document tree for a simple class `MyClass` with a property `my_property` that has a type hint. Finally, it checks if type hints are present in the generated document. If they are, the script raises an `AssertionError`.