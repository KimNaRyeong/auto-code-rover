Here is the reproducer script:

```python
import pyreverse
from your_module import C  # Replace 'your_module' with the actual module name where you defined class C

def main():
    try:
        # Call the method that should raise an error when type hints are not used
        c = C()
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected pyreverse to read type hints"

if __name__ == "__main__":
    main()
```

Please replace `'your_module'` with the actual module name where you defined class `C`.