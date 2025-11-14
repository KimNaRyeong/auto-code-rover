Here is the reproducer.py file:
```
import os
from sphinx.application import Sphinx
from sphinx.ext.autodoc import AutodocDirective
from docutils.parsers.rst import Directive, directives
from docutils.nodes import paragraph, literal_block

def setup(app):
    app.add_directive('listing', ListingDirective)

class ListingDirective(Directive):
    has_content = True

    def run(self):
        self.assert_has_content()
        text = '\n'.join(self.content)
        node = literal_block(text, text)
        return [node]

def test_latex_issue():
    srcdir = os.path.dirname(__file__)
    outdir = os.path.join(srcdir, '_build', 'latex')
    app = Sphinx(srcdir, srcdir, outdir, outdir, 'latex', ['sphinx.ext.autodoc'])
    app.builder.supported_image_types = []  # Disable image generation
    app.setup()

    with open(os.path.join(srcdir, 'input.rst'), 'w') as f:
        f.write("""
.. listing::

   :samp:`{file}.cc` :samp:`{file}.cp` :samp:`{file}.cxx` :samp:`{file}.cpp` :samp:`{file}.CPP` :samp:`{file}.c++` :samp:`{file}.C`
  C++ source code that must be preprocessed.  Note that in :samp:`.cxx`,
  the last two letters must both be literally :samp:`x`.  Likewise,
  :samp:`.C` refers to a literal capital C.

   :samp:`{file}.mm` :samp:`{file}.M`
  Objective-C++ source code that must be preprocessed.

   :samp:`{file}.mii`
  Objective-C++ source code that should not be preprocessed.

   :samp:`{file}.hh` :samp:`{file}.H` :samp:`{file}.hp` :samp:`{file}.hxx` :samp:`{file}.hpp` :samp:`{file}.HPP` :samp:`{file}.h++` :samp:`{file}.tcc`
  C++ header file to be turned into a precompiled header or Ada spec
""")

    app.build()

    with open(os.path.join(outdir, 'latex', 'input.tex'), 'r') as f:
        latex_content = f.read()
        assert '\\newline' in latex_content, "Terms are not separated by a newline"
        print("Issue is fixed!")

try:
    test_latex_issue()
except Exception as e:
    print_stacktrace(e)
    raise SystemExit(1)
```
This script sets up a Sphinx project with the `autodoc` extension and a custom directive `listing`. It then writes an input file in RST format, builds the LaTeX output, and checks if the terms are separated by a newline character (`\\newline`) in the generated TeX file. If not, it raises an `AssertionError`.