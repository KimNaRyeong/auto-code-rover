Here is the reproducer script:

```python
import os
from sphinx.application import SphinxApplication
from sphinx.config import Config

def main():
    config = Config()
    app = SphinxApplication(config)

    source_dir = 'source'
    output_dir = 'build'

    if not os.path.exists(source_dir):
        os.makedirs(source_dir)

    with open(os.path.join(source_dir, 'index.rst'), 'w') as f:
        f.write('.. toctree::\n')
        f.write('   a.md\n')

    with open(os.path.join(source_dir, 'a.md'), 'w') as f:
        pass

    with open(os.path.join(source_dir, 'a.rst'), 'w') as f:
        pass

    try:
        app.build()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected error")

if __name__ == "__main__":
    main()
```

This script creates a simple Sphinx project with two files `a.md` and `a.rst`, both named the same but with different extensions. It then tries to build the project, which should raise an exception due to the unexpected behavior. The script prints the stack trace of the error and raises an `AssertionError`.