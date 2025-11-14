Here is the reproducer script:

```python
import numpy as np
from sklearn.preprocessing import LabelEncoder

def reproduce_issue():
    le = LabelEncoder()
    le.fit(["a", "b"])
    try:
        le.transform([])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

To run the script, save it to a file named `reproducer.py` and execute it with Python 3.6.3:

```bash
python3 reproducer.py
```

This should print the stack trace of the issue and raise an AssertionError.