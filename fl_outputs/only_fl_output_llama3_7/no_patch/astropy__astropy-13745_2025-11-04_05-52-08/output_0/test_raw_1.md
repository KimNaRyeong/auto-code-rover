Here is the reproducer script:

```python
import numpy as np
from astropy.coordinates import Latitude

def main():
    try:
        lat = np.float32(np.pi/2)
        Latitude(lat, 'rad')
    except ValueError as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

if __name__ == "__main__":
    main()
```

This script will run and reproduce the issue. If you run this script and it doesn't raise an `AssertionError`, then the issue is fixed.