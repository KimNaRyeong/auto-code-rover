Below is a Python script designed as `reproducer.py`, which attempts to reproduce the issue described regarding the incorrect legend values when plotting large ranges in seaborn with matplotlib backend. This script is structured to raise an `AssertionError` if the issue is detected (i.e., when the multiplicative offset value is not included in legends for large ranges). It utilizes `matplotlib` to manually check the format of the tick labels after the plot has been created. This requires a deeper inspection into the objects created by seaborn and matplotlib to find the legend and assess its correctness.

```python
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

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import numpy as np

    # Make sure the mpl and sns versions are compatible with this script
    assert "matplotlib" in sys.modules, "matplotlib is required"
    assert "seaborn" in sys.modules, "seaborn is required"

    # Load or create a dataset
    np.random.seed(42)
    data = pd.DataFrame({
        'bill_length_mm': np.random.rand(100) * 50 + 30,  # Random data for illustration
        'bill_depth_mm': np.random.rand(100) * 20 + 15,
        'body_mass_g': np.random.rand(100) * 2500 + 3000,
        'species': np.random.choice(['Adelie', 'Chinstrap', 'Gentoo'], 100)
    })
    data["body_mass_mg"] = data["body_mass_g"] * 1000

    # Create a plot
    p = sns.scatterplot(data=data, x="bill_length_mm", y="bill_depth_mm",
                        hue="species", size="body_mass_mg",
                        sizes=(20, 200))

    plt.legend(title='Body Mass (mg)')

    # Assuming the legend is created with ScalarFormatter and large values should trigger an offset
    # Let's manually verify that an offset is applied in the legend's title
    legend = [t.get_text() for t in p.get_legend().get_texts()]
    assert any("1e6" in text for text in legend), "Legend does not contain the expected offset notation '1e6'"

except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)  # Exit with error status because the issue is present

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)  # Exit with error status due to an unexpected error

print("Issue is fixed, or the test did not reproduce the issue.")
sys.exit(0)  # Exit with success status
```

This script is designed to work on a standard setup where seaborn and matplotlib are installed. It incorporates an `AssertionError` based on an explicit check for the inclusion of an offset indication (`'1e6'`) in the legend, which directly relates to the original issue's description of incorrect legend values for plots with large ranges. The script includes structured exception handling to catch and report errors accurately, including custom logic to expose the exact location and nature of encountered issues.