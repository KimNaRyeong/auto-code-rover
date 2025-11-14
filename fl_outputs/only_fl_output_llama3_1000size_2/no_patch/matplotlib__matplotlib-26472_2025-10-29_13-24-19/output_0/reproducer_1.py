import matplotlib.pyplot as plt
from contextlib import contextmanager

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

@contextmanager
def window(block=False):
    plt.switch_backend('QT5')
    plt.ioff()
    yield
    plt.show()
    plt.ion()
    plt.switch_backend('inline')

try:
    with window():
        plt.plot([1, 3, 2])
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    try:
        with open(StringIO(), 'w') as f:
            with redirect_stdout(f):
                # Your code here
                pass
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")
