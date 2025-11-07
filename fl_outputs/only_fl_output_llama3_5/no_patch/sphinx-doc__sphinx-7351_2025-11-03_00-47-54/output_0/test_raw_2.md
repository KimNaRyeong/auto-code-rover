Here is the reproducer script:

```python
import os
from sphinx.application import SphinxApplication
from sphinx.config import Config
from sphinx.util import logging

def main():
    config = Config()
    app = SphinxApplication(config)

    # Create a sample project directory
    project_dir = "docs"
    os.makedirs(project_dir, exist_ok=True)
    os.chdir(project_dir)

    # Create the files
    with open("index.rst", "w") as f:
        f.write(".. toctree::\n    a.md\n")
    with open("a.md", "w") as f:
        pass
    with open("a.rst", "w") as f:
        pass

    # Try to build the project
    try:
        app.build()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not reproduced")

if __name__ == "__main__":
    main()
```

This script creates a sample Sphinx project directory, writes the necessary files (index.rst and two files with the same name but different extensions), and then tries to build the project. If the issue is present, it should raise an `AssertionError` and print the stack trace using the provided function.

Please note that you may need to adjust the script according to your specific requirements or environment.