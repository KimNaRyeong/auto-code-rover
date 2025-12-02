 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import os
import sys
import sphinx
import sphinx.ext.autodoc as autodoc
import sphinx.ext.napoleon as napoleon
import sphinx.ext.todo as todo
import sphinx.application as application
import sphinx.builders.html as html_builder
import sphinx.environment as environment
import sphinx.writers.html as html_writer
import sphinx.roles as roles
import sphinx.highlighting as highlighting
import sphinx.addnodes as addnodes
import sphinx.domains.python as python_domain
import sphinx.directives.code as code_directive
import sphinx.directives.other as other_directives
import sphinx.directives.patches as patches_directives
import sphinx.directives.html as html_directives
import sphinx.builders.latex as latex_builder
import sphinx.writers.latex as latex_writer
import sphinx.domains.std as std_domain
import sphinx.environment.adapters.toctree as toctree_adapter
import sphinx.ext.mathjax as mathjax
import sphinx.ext.ifconfig as ifconfig
import sphinx.ext.jsmath as jsmat
import sphinx.ext.viewcode as viewcode
import sphinx.ext.doctest as doctest
import sphinx.ext.inheritance_diagram as inheritance_diagram
import sphinx.ext.graphviz as graphviz
import sphinx.ext.linkcode as linkcode
import sphinx.ext.intersphinx as intersphinx
import sphinx.ext.autosectionlabel as autosectionlabel
import sphinx.ext.coverage as coverage
import sphinx.ext.imgmath as imgmath
import sphinx.ext.latexpdf as latexpdf
import sphinx.ext.extlinks as extlinks
import sphinx.ext.githubpages as githubpages
import sphinx.ext.mathbase as mathbase
import sphinx.ext.googleanalytics as googleanalytics
import sphinx.ext.sphinxapidoc as sphinxapidoc
import sphinx.ext.doctreesearch as doctree_search
import sphinx.ext.opengraph as opengraph
import sphinx.ext.jsonschema as jsonschema
import sphinx.ext.epub as epub
import sphinx.ext.bibtex as bibtex
import sphinx.ext.only as only
import sphinx.ext.smartquotes as smartquotes
import sphinx.ext.sphinxcontrib.plantuml as plantuml
import sphinx.ext.sphinxcontrib.confluencebuilder as confluencebuilder
import sphinx.ext.sphinxcontrib.qthelp as qthelp
import sphinx.ext.sphinxcontrib.devhelp as devhelp
import sphinx.ext.sphinxcontrib.serializinghtml as serializinghtml
import sphinx.ext.sphinxcontrib.htmlhelp as htmlhelp
import sphinx.ext.sphinxcontrib.jsmath as jsmath_extension
import sphinx.ext.sphinxcontrib.restbuilder as restbuilder
import sphinx.ext.sphinxcontrib.applehelp as applehelp
import sphinx.ext.sphinxcontrib.servedownload as servedownload
import sphinx.ext.sphinxcontrib.programoutput as programoutput
import sphinx.ext.sphinxcontrib.spelling as spelling
import sphinx.ext.sphinxcontrib. tobacco as tobacco
import sphinx.ext.sphinxcontrib.actdiag as actdiag
import sphinx.ext.sphinxcontrib.blockdiag as blockdiag
import sphinx.ext.sphinxcontrib.nwdiag as nwdiag
import sphinx.ext.sphinxcontrib.packetdiag as packetdiag
import sphinx.ext.sphinxcontrib.seqdiag as seqdiag
import sphinx.ext.sphinxcontrib.rackdiag as rackdiag
import sphin