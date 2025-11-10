Here is the reproducer script:

```py
import json
from functools import lru_cache

@lru_cache()
def object():
    return "foo"

def test_json_encoder():
    try:
        assert (object:="foo") in json.dumps(object())
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    test_json_encoder()
```

This script will raise an `UnboundLocalError` when the issue is present and print a stack trace of the issue.