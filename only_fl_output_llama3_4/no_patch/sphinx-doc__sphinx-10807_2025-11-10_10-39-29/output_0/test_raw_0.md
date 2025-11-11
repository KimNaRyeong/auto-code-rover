Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import sphinx
from sphinx.ext import autodoc

def main():
    # Create a test module with docstrings and functions
    mod = "mod"
    submod = "submod"

    class Mod:
        def function(self):
            pass

        def another_function(self):
            pass

    class SubMod:
        def function2(self):
            pass

    __doc__ = f"""
    {mod}
    =========

    This is the module docstring.

    Header
    ======

    .. autofunction:: {mod}.function
    .. autofunction:: {mod}.another_function

    {submod}
    =========

    This is the sub-module docstring.

    Subheader
    ==========

    .. autofunction:: {submod}.{function2}
    """

    # Create a test Sphinx environment
    env = sphinx.environment.Environment()
    env.add_object(mod, Mod())
    env.add_object(submod, SubMod())

    # Generate the TOC entry for each function and method
    toc_entry = f"""
    .. toctree::
       :maxdepth: 2

       {mod}.function
       {mod}.another_function
       {submod}.{function2}
    """

    print(toc_entry)

if __name__ == "__main__":
    main()
```

This script creates a test module with docstrings and functions, then generates the TOC entry for each function and method using Sphinx's autodoc extension. The output should show that the functions are placed under the module headers in the TOC, which is not the expected behavior.

To reproduce the issue, simply run the script: `python3 reproducer.py`.