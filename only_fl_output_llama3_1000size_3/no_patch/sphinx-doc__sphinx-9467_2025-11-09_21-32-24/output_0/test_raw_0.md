Here is the reproducer script:

```python
import sphinx
from sphinx.application import SphinxApplication
from sphinx.util.docutils import document_nodes

def main():
    app = SphinxApplication()
    app.builder = sphinx.builders.LinkcheckBuilder(app, config=None)

    rst_str = r"""
.. _`OpenSSL's test vectors`: https://github.com/openssl/openssl/blob/97cf1f6c2854a3a955fd7dd3a1f113deba00c9ef/crypto/evp/evptests.txt#L232
"""

    try:
        app.builder.build_string(rst_str)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Linkcheck failed")

if __name__ == "__main__":
    main()
```

This script creates a Sphinx application with the Linkcheck builder, then attempts to build a string containing the problematic rst code. If an exception is raised during this process (which should happen if the issue is present), it prints the stack trace and raises an AssertionError.