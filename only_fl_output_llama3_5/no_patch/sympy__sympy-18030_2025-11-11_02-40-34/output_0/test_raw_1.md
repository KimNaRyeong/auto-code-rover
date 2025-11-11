Here is the reproducer script:

```python
import scipy.interpolate as si

def interpolate(y, x):
    return si.interp1d(range(1, len(y)+1), y)(x)

y = (18, 25, 43, 70, 115)
try:
    result = interpolate(y, 5)
    assert not isinstance(result, float) or result == 115, "interpolate could provide value instead of nan"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue reproduced successfully")
exit(0)
```

You can run this script with `python3 reproducer.py` to reproduce the issue.