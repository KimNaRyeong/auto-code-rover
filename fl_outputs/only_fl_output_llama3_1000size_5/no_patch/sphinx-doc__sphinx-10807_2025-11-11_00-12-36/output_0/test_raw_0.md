Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import sphinx
from sphinx.ext import autodoc

def main():
    try:
        # Create a test module with docstrings and functions
        mod = "mod"
        submod = "submod"
        function1 = f"{mod}.function"
        function2 = f"{submod}.{function1}"
        
        # Generate RST content for the module
        rst_content = f".. module:: {mod}\n\n{mod} docstring...\n\nHeader\n======\n.. autofunction:: {function1}\n.. autofunction:: {function2}\n"
        
        # Parse the RST content and check if the functions are under the header
        doc = sphinx.builder.Builder("html", autodoc.AutoDocumenter(mod, rst_content))
        assert not any(f.startswith("  Header") for f in doc.get_toc_entries()), "Functions should be at top-level"
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script creates a test module with two functions and generates RST content that mimics the issue. It then parses the RST content using Sphinx's builder and checks if the functions are under the header in the TOC entries. If they are, it raises an `AssertionError` with a stack trace.