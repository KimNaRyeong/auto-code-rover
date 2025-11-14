python
import os
from sphinx.application import Sphinx
from sphinx.ext.autodoc import setup

# Create a temporary directory for the documentation build
tmp_dir = 'tmp_doc_build'
os.makedirs(tmp_dir, exist_ok=True)

# Initialize Sphinx application
app = Sphinx(srcdir=tmp_dir, confdir=tmp_dir, outdir=tmp_dir, doctreedir=tmp_dir)
setup(app)

# Define the classes to reproduce the issue
class RasterDataset:
    pass

class Landsat(RasterDataset):
    pass

# Add the classes to the documentation
app.add_autodocumenter_directive('autoclass', 'Landsat')

# Build the documentation
app.build()

# Check if the base class is correctly detected
with open(os.path.join(tmp_dir, '_build/html/api/Landsat.html'), 'r') as f:
    html_content = f.read()
    assert 'RasterDataset' in html_content, "Base class not correctly detected"
    print("Issue not present, exiting with code 0")
    os._exit(0)

except AssertionError as e:
    print_stacktrace(e)
    os._exit(1)
