Creating a standalone Python file to reproduce a documentation issue related to Sphinx (a tool primarily used for generating documentation for Python projects) is an unconventional request since the core issue revolves around Sphinx's handling of reStructuredText (reST) files, not Python code execution. However, I will draft a Python script designed to mimic the execution context of Sphinx and simulate document generation to illustrate how you might detect the described issue programmatically. Given the nature of the problem—which fundamentally requires processing reST documentation and not running Python code—the "assertion" here is a bit conceptual and indirect.

Here's a Python script that tries to capture the essence of your request, assuming Sphinx is part of the environment it will run in. This script will programmatically create a Sphinx project, add a file with the provided reST content, and then run Sphinx to see if the warnings are generated. The script interprets the presence of these warnings as an assertion failure.

```python
import subprocess
import os

def setup_sphinx_project():
    # Create a minimal Sphinx project setup
    try:
        os.mkdir('temp_docs')
    except FileExistsError:
        pass  # Directory already exists

    with open('temp_docs/conf.py', 'w') as f:
        # Minimal Sphinx configuration
        f.write("project = 'TestProject'\n")
        f.write("master_doc = 'index'\n")
        f.write("extensions = ['sphinx.ext.autodoc']\n")

    with open('temp_docs/index.rst', 'w') as f:
        # Insert the reST content that should lead to the bug
        f.write("""
.. py:class:: mod.A
.. py:class:: mod.submod.A

.. py:function:: f()

    - :py:class:`mod.A`
    - :py:class:`mod.submod.A`

    :param mod.A a:
    :param mod.submod.A b:
    :rtype: mod.A
    :rtype: mod.submod.A

.. py:currentmodule:: mod

.. py:function:: f()

    - :py:class:`A`
    - :py:class:`mod.A`
    - :py:class:`mod.submod.A`

    :param A a:
    :param mod.A b:
    :param mod.submod.A c:
    :rtype: A
    :rtype: mod.A
    :rtype: mod.submod.A

.. py:currentmodule:: mod.submod

.. py:function:: f()

    - :py:class:`A`
    - :py:class:`mod.A`
    - :py:class:`mod.submod.A`

    :param A a: BUG: links to mod.A instead of mod.submod.A
    :param mod.A b:
    :param mod.submod.A c:
    :rtype: A
    :rtype: mod.A
    :rtype: mod.submod.A
""")


def run_and_check():
    result = subprocess.run(['sphinx-build', '-b', 'html', 'temp_docs', 'temp_docs/_build'], text=True, capture_output=True)
    if "more than one target found for cross-reference 'A'" in result.stderr:
        raise AssertionError("Sphinx generated ambiguous class lookup warnings.")

def main():
    setup_sphinx_project()
    try:
        run_and_check()
        print("No issues detected—Sphinx did not generate expected warnings.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

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

if __name__ == '__main__':
    main()
```

**Note**: This script is conceptual and serves to illustrate the approach rather than provide a direct execution path for Sphinx documentation issues. Adjustments might be necessary to properly set up Sphinx environments or handle the cleanup of the created temporary files and directories.