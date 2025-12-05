 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sphinx
from sphinx.ext.autodoc import AncestorDoc

def setup(app):
    app.connect('autodoc-process-signature', process_signature)

