 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sphinx
import docutils
from sphinx.errors import SphinxError

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    # Load the glossary file
    glossary = docutils.readers.standalone.StandaloneReader().parse(
        # filename='doc/glossary.rst',  # Uncomment this line to use the real file
        filename='glossary.rst',  # Use this line to use the local file for testing
        parser=docutils.parsers.rst.Parser(),
        component_names=['glossary']
    )

    # Check for duplicate terms
    terms = {}
    for term in glossary.get('glossary', []):
        term_name = term['term'].lower()
        if term_name in terms:
            raise AssertionError(f"Duplicate term: {term_name}")
        terms[term_name] = term

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
To reproduce the issue, create a file named `glossary.rst` in the same directory as `reproducer.py` with the following content:
```rst
.. glossary::

   MySQL
      A relational database management system (RDBMS) based on SQL.

   mysql
      A client library for connecting to a MySQL server.

   SQL
      A standard language for managing and manipulating relational databases.
```
Then, execute the script with `python3 reproducer.py`. It should raise an `AssertionError` with a stack trace, indicating the duplicate term.

If the issue is fixed, the script should exit with code 0. In this case, you can remove the `glossary.rst` file and uncomment the `filename='doc/glossary.rst'` line in the `main()` function to use the real file for testing.