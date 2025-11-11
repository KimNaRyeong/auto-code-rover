Here is the reproducer script:

```python
import pytest
from conftest import bar

def test_0(bar):
    assert 0

@pytest.fixture
def bar():
    if True:
        pytest.skip("Skipping")

if __name__ == "__main__":
    try:
        pytest.main(["-rs", "-k", "test_0"])
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

This script should reproduce the issue.