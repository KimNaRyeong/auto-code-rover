Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import os
from babel.messages import frontend as babel
from sphinx.builders.gettext import GettextBuilder

def reproducer():
    # Create a temporary directory for the build
    tmp_dir = 'tmp_reproducer'
    os.makedirs(tmp_dir, exist_ok=True)

    # Initialize Sphinx builder
    builder = GettextBuilder(None)
    builder.init()

    # Process some sample files to generate the gettext catalog
    sample_files = [
        ('../../manual/modeling/hair.rst', 'msgid "Type"\nmsgstr ""'),
        ('../../manual/movie_clip/tracking/clip/toolbar/solve.rst', 'msgid "Type"\nmsgstr ""'),
        ('../../manual/physics/dynamic_paint/brush.rst', 'msgid "Type"\nmsgstr ""'),
    ]
    for file, content in sample_files:
        with open(os.path.join(tmp_dir, file), 'w') as f:
            f.write(content)

    # Run the gettext builder
    builder.build(None, tmp_dir)

    # Load the generated .pot file
    pot_file = os.path.join(tmp_dir, 'blender_manual.pot')
    catalog = babel.load_catalog('blender_manual', [pot_file], locale='en')

    # Check for duplicated locations
    for message in catalog:
        if len(set(message.locations)) != len(message.locations):
            print(f"Duplicated locations found: {message.locations}")
            raise AssertionError("Duplicated locations found")

    print("No issue found")

if __name__ == '__main__':
    try:
        reproducer()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
This script creates a temporary directory, initializes the Sphinx GettextBuilder, processes some sample files to generate the gettext catalog, loads the generated .pot file, and checks for duplicated locations. If duplicated locations are found, it raises an `AssertionError` with a stack trace of the issue.