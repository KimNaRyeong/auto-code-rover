```python
#!/usr/bin/env python3
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import tempfile
import os
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

def check_sketch_effect_in_file(filepath: str) -> bool:
    """
    A simple, imperfect heuristic to see if sketch effect might be present in a pgf output.
    This doesn't parse the file with full accuracy but looks for specific strings that
    should only be present if the sketch effect was attempted to be applied.
    Returns True if the effect seems to be present, False otherwise.
    """
    try:
        with open(filepath, "r") as file:
            content = file.read()
            # This is a very basic check, and might not work for all cases,
            # especially if the internals of how the sketch effect is implemented change.
            # More robust checking might be needed for a real-world scenario.
            return "decorate" in content or "decoration" in content
    except Exception as e:
        print_stacktrace(e)
        return False

def test_sketch_params_ignored():
    mpl.use("pgf")
    
    mpl.rcParams.update({
        'font.family': 'serif',
        'text.usetex': True,
        'pgf.rcfonts': False,
        'pgf.preamble': [ 
                #r"\usepackage{pgf}",
                #r"\usepgfmodule{decorations}",
                #r"\usepgflibrary{decorations.pathmorphing}",
        ],
    })
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range(10))
    
    ax.spines["bottom"].set_sketch_params(scale=5, length=10, randomness=42)
    
    with tempfile.TemporaryDirectory() as tmpdirname:
        filepath = os.path.join(tmpdirname, "foo.pgf")
        fig.savefig(filepath)
        # Check if the saved file has effects of the sketch parameters
        if not check_sketch_effect_in_file(filepath):
            raise AssertionError("Sketch params appear to be ignored with PGF backend")

try:
    test_sketch_params_ignored()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    print("Issue not found, the sketch params are applied as expected.")
    sys.exit(0)
```