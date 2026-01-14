 Based on the issue description, it seems like the warning is raised when Sphinx is unable to resolve a cross-reference to a class or module in the documentation. In this case, it appears to be related to the ellipsis (`...`) used in the `trio_main` method's signature in `qtrio/_core.py`.

To reproduce the issue, you can create a minimal reproducer as follows:

1. Create a new directory for the reproducer and navigate into it:
```bash
mkdir qtrio-reproducer
cd qtrio-reproducer
```
2. Create a file named `qtrio/_core.py` with the following content:
```python
class Outcomes:
    """Outcomes for async operations."""

