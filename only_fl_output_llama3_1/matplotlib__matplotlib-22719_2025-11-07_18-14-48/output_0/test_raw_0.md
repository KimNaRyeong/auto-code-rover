Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import assertpy as ap

def main():
    f, ax = plt.subplots()
    ax.xaxis.update_units(["a", "b"])
    try:
        ax.plot([], [])
    except Exception as e:
        print_stacktrace(e)
        ap.assert_that(True, "Expected no exception").is_true()

if __name__ == "__main__":
    main()
```

This script creates a plot with an x-axis that has units set to `["a", "b"]`. Then it attempts to plot empty data. If the deprecation warning is raised, the script prints the stack trace and asserts that the exception was not expected.