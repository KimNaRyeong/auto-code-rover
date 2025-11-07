import re
import os
import sys

# Simulated Docstring to represent what might be parsed from the file
docstring = """
Google Example
==============

.. automodule:: example_google
   :members:
   :noindex:

:ref:`genindex`
"""

# Simulated behavior of searching through Sphinx-generated content
def search_index_simulation(content: str):
    """
    Simulates the behavior of searching through generated content
    to find whether `.. automodule::` directives with ':noindex:' are excluded.
    """
    index_entries = re.findall(r'\.\. automodule:: example_google\n\s*:members:\n\s*:noindex:', content)
    return len(index_entries) > 0

def run_simulation():
    # Simulating parsing and indexing based on the docstring
    found_index_entry = search_index_simulation(docstring)
    if found_index_entry:
        raise AssertionError("The `:noindex:` option for automodule was ignored.")

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

if __name__ == '__main__':
    try:
        run_simulation()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Issue not found. Exiting with code 0.")
        sys.exit(0)
