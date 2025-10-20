Under the given constraint and the nature of the issue, it's clear that crafting a standalone Python reproducer for an issue that inherently involves interactive Jupyter Notebook behavior and GUI elements presents significant challenges. The issue hinges on dynamically switching between matplotlib backends within an interactive environment and observing the effect on GUI windows. Such interactions are outside the typical scope of a simple, non-interactive, script-based execution model.

However, striving to meet the requirements and acknowledging the limitations, I'll provide a hypothetical `reproducer.py` script. This script aims to simulate the issue as closely as possible under the circumstances, though it's important to note that executing this script outside an environment like Jupyter Notebook might not faithfully reproduce the GUI-related aspects of the issue. Specifically, the script cannot simulate the opening and closing of GUI windows in a command-line environment.

That said, this Python script attempts to capture the essence of switching between backends and uses assertions to identify if the required conditions (i.e., backend being effectively switched without closing GUI windows) are met ideally. For genuine verification, running this in a compatible interactive environment and adapting the script to such an environment's capabilities would be necessary.

```python
# reproducer.py
import matplotlib.pyplot as plt
import matplotlib
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_backend_switch():
    try:
        # Initial backend is typically 'inline' in a Jupyter Notebook
        initial_backend = matplotlib.get_backend()
        
        # Switch to 'qt5agg', simulating the opening of a GUI window
        matplotlib.use('Qt5Agg')
        plt.plot([1, 2, 3])  # This might open a GUI window, if possible
        
        # Switch back to 'inline', checking if the GUI window is affected
        matplotlib.use('inline')
        
        # Verify the backend was switched back
        current_backend = matplotlib.get_backend()
        assert current_backend == 'inline', "Backend did not switch back to 'inline'."
        
        # If no errors have occurred up to this point, it's assumed the GUI window behavior is as expected
        print("Success: Backend switching did not close GUI windows unexpectedly.")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    test_backend_switch()
```

Keep in mind, this script does not fully encapsulate the interactive and GUI aspects of the originally described issue due to its execution outside a Jupyter Notebook or similar interactive environment.

To truly verify the fix or continued presence of the issue, one would need to adapt this logic into a context that supports interactive plotting (like a Jupyter Notebook) and observe the GUI behavior directly.