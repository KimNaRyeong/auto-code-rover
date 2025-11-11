Here is the reproducer script:

```python
import seaborn as sns
import seaborn.objects as so
import pandas as pd

def main():
    penguins = sns.load_dataset("penguins")
    try:
        (
            so.Plot(penguins.dropna(), x="sex", y="bill_depth_mm")
            .add(so.Dots())
            .facet(col="species", row="island")
        )
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```

This script will reproduce the issue and print a stack trace.