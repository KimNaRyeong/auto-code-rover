Here is the reproducer script:

```py
import json
import pytest

def test_json_encoder():
    try:
        assert (object:="foo") in json.dumps(object)
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    test_json_encoder()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.