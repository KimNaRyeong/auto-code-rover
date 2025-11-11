Here is the reproducer script:

```python
import sphinx
from sphinx.application import SphinxApplication
from sphinx.util import logging

def main():
    app = SphinxApplication()
    app.builder = sphinx.builders.LinkcheckBuilder(app, config_file='conf.py')
    app.config.master_doc = 'index'
    app.config.linkcheck_ignore = ['_OpenSSL\'s test vectors: https://github.com/openssl/openssl/blob/97cf1f6c2854a3a955fd7dd3a1f113deba00c9ef/crypto/evp/evptests.txt#L232']
    try:
        app.build()
    except sphinx.errors.LinkcheckError as e:
        print_stacktrace(e)
        raise AssertionError("Linkcheck failed")

if __name__ == "__main__":
    main()
```

This script creates a Sphinx application with the Linkcheck builder, sets up the configuration to match the issue description, and then attempts to build the linkcheck. If an error occurs during the build process (which should happen when trying to check the broken link), it prints the stack trace using the provided function and raises an `AssertionError`.