Here is the reproducer script:

```python
def interpolate(y, x):
    y = list(y)
    f = interp1d(range(1, len(y)+1), y)
    return f(x)

y = [18, 25, 43, 70, 115]
try:
    result = interpolate(y, 5)
    assert np.isnan(result) == False, "Expected value instead of nan"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue fixed")
    exit(0)
```

This script will raise an `AssertionError` when the issue is present and print a stack trace. If the issue is fixed, it will print "Issue fixed" and exit with code 0.