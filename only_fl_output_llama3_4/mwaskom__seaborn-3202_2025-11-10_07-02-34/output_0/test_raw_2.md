Here is the reproducer script:

```python
import seaborn as sns
import pandas as pd

def main():
    penguins = sns.load_dataset("penguins")
    try:
        plot = (
            sns.objects.Plot(penguins.dropna(), x="sex", y="bill_depth_mm")
            .add(sns.objects.Dots())
            .facet(col="species", row="island")
        )
        print(plot)
    except Exception as e:
        print_stacktrace(e)
        raise

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

if __name__ == "__main__":
    main()
```

This script will reproduce the issue and print a stack trace.