import matplotlib.backends.backend_pdf
import os

def test_keep_empty_default():
    pdf = matplotlib.backends.backend_pdf.PdfPages("test.pdf")
    pdf.close()
    assert os.path.exists("test.pdf"), "PDF file was not created"
    with open("test.pdf", 'rb') as f:
        content = f.read()
    assert len(content) > 0, "PDF file is empty"

try:
    test_keep_empty_default()
except AssertionError as e:
    print_stacktrace(e)
    os._exit(1)

os.remove("test.pdf")
print("Issue not present, exiting with code 0")
os._exit(0)
