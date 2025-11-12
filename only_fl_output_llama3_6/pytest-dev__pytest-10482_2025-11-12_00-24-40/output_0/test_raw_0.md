Here is the reproducer script:

```python
import pytest
from conftest import bar

def test_0():
    assert 0

@pytest.fixture
def bar():
    if True:
        pytest.skip("Skipping")

if __name__ == "__main__":
    try:
        pytest.main([__file__, "-rs"])
    except Exception as e:
        print_stacktrace(e)
        raise
```

You can run this script with `python3 reproducer.py` to reproduce the issue.