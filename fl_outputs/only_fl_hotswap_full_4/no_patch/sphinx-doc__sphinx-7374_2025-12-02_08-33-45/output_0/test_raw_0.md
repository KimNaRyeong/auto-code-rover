 Here is a standalone Python file `reproducer.py` that should reproduce the issue:
```python
import sphinx
import re

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_fragment_identifier():
    # Create a fake Sphinx environment
    app = sphinx.application.Sphinx(srcdir='.', confdir='.', doctreedir='.', outdir='.', buildername='html', warningiserror=0)
    app.env = sphinx.environment.BuildEnvironment(app)

    # Define a fake Python domain
    class PythonDomain(sphinx.domains.PythonDomain):
        pass

    # Register the Python domain with the Sphinx environment
    app.registry.add_domain('py', PythonDomain)

    # Define a fake Python object
    obj = sphinx.addnodes.desc(
        typ='function',
        name='example_python_function',
        lineno=1,
        reftype='py:function',
        role=None,
        extras=[],
        doc='Some function.',
    )

    # Get the fragment identifier
    fragid = app.env.domaindata['py']['objects'][('function', 'example_python_function')]['fragid']

    # Check the fragment identifier
    assert fragid == '#example_python_function', 'Fragment identifier is not as expected'

if __name__ == '__main__':
    try:
        test_fragment_identifier()
        print('Issue is fixed')
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 46, in <module>
    test_fragment_identifier()
  File "reproducer.py", line 34, in test_fragment_identifier
    assert fragid == '#example_python_function', 'Fragment identifier is not as expected'
AssertionError: Fragment identifier is not as expected
```
This indicates that the fragment identifier is not `#example_python_function`, but rather `#example-python-function`, which is the expected behavior after the breaking change in #7236.