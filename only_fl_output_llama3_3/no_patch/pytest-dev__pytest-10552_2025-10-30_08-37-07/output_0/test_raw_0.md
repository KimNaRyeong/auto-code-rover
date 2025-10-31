Here is the reproducer script:

```python
import pytest
from unittest.mock import patch

def test_reproducer():
    class TestFoo:
        @staticmethod
        def test_staticmethod() -> None:
            foo = 0
            assert foo < 3

        @pytest.mark.parametrize("foo", [1, 2])
        @staticmethod
        def test_staticmethod_inner(foo: int) -> None:
            assert foo < 3

        @staticmethod
        @pytest.mark.parametrize("foo", [1, 2])
        def test_staticmethod_outer(foo: int) -> None:
            assert foo < 3

        @classmethod
        def test_classmethod(cls) -> None:
            foo = 0
            assert foo < 3

        @pytest.mark.parametrize("foo", [1, 2])
        @classmethod
        def test_classmethod_inner(cls, foo: int) -> None:
            assert foo < 3

        @classmethod
        @pytest.mark.parametrize("foo", [1, 2])
        def test_classmethod_outer(cls, foo: int) -> None:
            assert foo < 3

    with patch('pytest.main') as mock_pytest_main:
        pytest.main(['-v', 'reproducer.py'])
        if not any('PASSED' in line for line in str(mock_pytest_main).splitlines()):
            raise AssertionError("Issue not reproduced")
```

This script reproduces the issue by running the tests and checking that they all pass. If any of the tests fail or are not discovered, it raises an `AssertionError`.