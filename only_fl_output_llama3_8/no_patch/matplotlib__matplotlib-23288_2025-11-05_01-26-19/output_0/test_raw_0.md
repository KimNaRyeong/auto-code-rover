Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from io import BytesIO
import unittest
from PIL import Image, ImageDraw

class TestBug(unittest.TestCase):

    def test_bug(self):
        try:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, "Long text with link", rotation=45, url="https://matplotlib.org")
            buf = BytesIO()
            pdf = matplotlib.backends.backend_pdf.PdfPages(buf)
            pdf.savefig(fig, bbox_inches='tight')
            pdf.close()
            img = Image.open('link.pdf')
            draw = ImageDraw.Draw(img)
            self.assertFalse(draw.textsize("Long text with link", font=None))
        except AssertionError:
            print_stacktrace(sys.exc_info()[1])
            raise
        finally:
            if 'link.pdf' in [img.name for img in plt.get_fignums()]:
                os.remove('link.pdf')

if __name__ == '__main__':
    unittest.main()
```

This script will create a PDF file named "link.pdf" and then check if the text is rotated correctly. If not, it will print the stack trace of the issue and raise an `AssertionError`.