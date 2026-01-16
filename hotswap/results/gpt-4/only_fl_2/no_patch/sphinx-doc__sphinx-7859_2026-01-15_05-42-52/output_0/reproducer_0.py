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

def test_sphinx_build_with_autodoc_typehints_descriptions():
    import subprocess
    import os

    # Setup minimal Sphinx project.
    os.makedirs("test_project/doc", exist_ok=True)
    with open("test_project/doc/source.conf.py", 'w') as conf:
        conf.write('''
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
project = 'Test Project'
master_doc = 'index'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
napoleon_use_ivar = True
autodoc_typehints = 'descriptions'
''')

    with open("test_project/doc/index.rst", 'w') as index:
        index.write('''
Welcome to Test Project's documentation!
========================================

.. automodule:: test_module
   :members:
   :undoc-members:
   :show-inheritance:
''')

    os.makedirs("test_project/test_module", exist_ok=True)
    with open("test_project/test_module/__init__.py", 'w') as mod_init:
        mod_init.write('''
"""Example module."""

def example_function(param1: int) -> bool:
    """Example function.

    :param param1: Description of param1.
    :type param1: int
    :return: Description of return value.
    :rtype: bool
    """
    return bool(param1)
''')

    try:
        # Build the documentation.
        subprocess.check_call(['sphinx-build', '-M', 'html', 
                               'test_project/doc', 'test_project/_build'])
    except subprocess.CalledProcessError as e:
        print_stacktrace(e)
        assert False, "Sphinx build failed."
    except Exception as e:
        print_stacktrace(e)
        assert False, f"Unexpected error encountered: {e}"

if __name__ == "__main__":
    test_sphinx_build_with_autodoc_typehints_descriptions()
    print("Test completed successfully, no issue detected.")
