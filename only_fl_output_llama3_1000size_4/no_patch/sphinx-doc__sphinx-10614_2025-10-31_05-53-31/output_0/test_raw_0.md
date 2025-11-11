Here is the reproducer script:

```python
import os
import sphinx
from sphinx.application import SphinxApplication
from sphinx.ext.inheritance_diagram import InheritanceDiagram

def generate_inheritance_diagram(app: SphinxApplication, docname: str):
    app.builder.build_all()
    diagram = InheritanceDiagram(app.builder.env, 'my_package', 'index')
    with open('docs_source/inheritance_diagram.svg', 'w') as f:
        f.write(diagram.as_svg())

def check_links():
    os.chdir('docs_build')
    try:
        os.system('firefox http://localhost:63342/sphix_svg_bug/docs_build/index.html')
        os.system('firefox http://localhost:63342/sphix_svg_bug/docs_build/my_package/index.html')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Links in SVG file are not working")

def main():
    app = SphinxApplication()
    app.builder.config.set_value('html_static_path', ['_static'])
    generate_inheritance_diagram(app, 'index')
    check_links()

if __name__ == "__main__":
    main()
```

This script will create an inheritance diagram in SVG format and then try to open the links in Firefox. If any of the links do not work (i.e., a 404 page is displayed), it will print the stack trace and raise an `AssertionError`.