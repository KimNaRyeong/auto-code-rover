Given the constraints and the request for a standalone Python script to reproduce the issue, let's rewrite the `reproducer.py` script considering the environment constraint (e.g., non-Jupyter environment). Importantly, the `%matplotlib inline` directive is not valid syntax in a standalone script, as it's specific to IPython environments like Jupyter notebooks. Here's a revised version:

```python
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

def main():
    import matplotlib
    import networkx as nx
    import matplotlib.pyplot as plt

    assert matplotlib.__version__ == '3.5.0', f"Test is for matplotlib version 3.5.0, but found version {matplotlib.__version__}"

    # Generate a random graph using networkx
    G = nx.erdos_renyi_graph(10, 0.5)

    try:
        nx.draw(G)
        plt.show()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Failed to display graph correctly with matplotlib 3.5.0") from e

if __name__ == "__main__":
    main()
```

This script attempts to generate and display a simple graph using `matplotlib` and `networkx`. 

- Firstly, it checks the version of matplotlib to ensure it matches version `3.5.0`, as described in the problem statement. If not, it raises an assertion error.
- If the test proceeds but fails to display the graph as expected (an outcome that might differ depending on environment capabilities and what "not working well" precisely means in this context), it captures and prints the exception stack trace.

Note: Given the original error was observed in a Jupyter environment and reproduced here in a standalone script, this script makes an assumption that the environment can handle `plt.show()` (which may not work as expected in headless environments without a GUI). If running in an environment without a display (e.g., a server), you might not see the plot and could consider saving the plot to a file instead (`plt.savefig('output.png')`) to validate the rendering issue.