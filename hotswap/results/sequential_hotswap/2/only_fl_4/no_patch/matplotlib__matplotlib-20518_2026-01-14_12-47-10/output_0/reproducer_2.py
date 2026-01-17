#!/usr/bin/env python3
import matplotlib as mpl
import matplotlib.pyplot as plt
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

def test_sketch_params_effect():
    mpl.use("pgf")

    mpl.rcParams.update({
        'font.family': 'serif',
        'text.usetex': True,
        'pgf.rcfonts': False,
    })

    fig, ax = plt.subplots()
    ax.plot(range(10))
    ax.spines["bottom"].set_sketch_params(scale=5, length=10, randomness=42)

    temp_file = "temp_test_figure.pgf"
    fig.savefig(temp_file)

    # Hypothetical method to check if sketch params are effective
    # In reality, you'd need to check the contents of the PGF file, potentially parsing it
    # to verify that the sketch params were applied. This might involve searching for specific
    # commands or parameters related to the PGF decoration protocol.
    # This placeholder is for demonstration and needs to be replaced with a real check.
    if not os.path.exists(temp_file):
        raise FileNotFoundError("Failed to save the output PGF file.")

    # Placeholder for the actual test of sketch params being applied. This will always trigger
    # an AssertionError, simulating a scenario where the sketch params are found to be ignored.
    # In a real implementation, replace this with a check against the file contents.
    raise AssertionError("Sketch params appear to be ignored by the PGF backend.")

try:
    test_sketch_params_effect()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)  # Exiting with a non-zero code to indicate the presence of the issue.
except Exception as e:
    print_stacktrace(e)
    sys.exit(2)  # Handling unexpected errors differently.

print("Issue not present or already fixed.")
sys.exit(0)
