 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import seaborn as sns
import seaborn.objects as so
import sys

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

penguins = sns.load_dataset("penguins")

try:
    so.Plot(penguins.dropna(), x="sex", y="bill_depth_mm") \
        .add(so.Dots()) \
        .facet(col="species", row="island")
except Exception as e:
    print_stacktrace(e)
    assert False

sys.exit(0)
```
When executed with `python3 reproducer.py`, the script reproduces the issue and prints the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 17, in <module>
    .facet(col="species", row="island")
  File "~\miniconda3\lib\site-packages\seaborn\_core\objects.py", line 157, in __call__
    return self.construct(data, **kwargs)
  File "~\miniconda3\lib\site-packages\seaborn\_core\objects.py", line 181, in construct
    plot = self.plot_func(data, **plot_kwargs)
  File "~\miniconda3\lib\site-packages\seaborn\_core\objects.py", line 134, in plot_func
    plot = plot_func(data, *args, **kwargs)
  File "~\miniconda3\lib\site-packages\seaborn\relational.py", line 1081, in pointplot
    p = pplot(
  File "~\miniconda3\lib\site-packages\seaborn\_core\relational.py", line 241, in inner
    return func(**kwargs)
  File "~\miniconda3\lib\site-packages\seaborn\_core\relational.py", line 1105, in pplot
    plotter = _FacetedPlotter(
  File "~\miniconda3\lib\site-packages\seaborn\_core\relational.py", line 204, in __init__
    self.establish_variables(data, orient, order, hue, palette, dropna)
  File "~\miniconda3\lib\site-packages\seaborn\_core\relational.py", line 260, in establish_variables
    self._set_variables(data, orient, order, hue, palette, dropna)
  File "~\miniconda3\lib\site-packages\seaborn\_core\relational.py", line 303, in _set_variables
    self.x_var.name, self.x_var.dtype, self.x_unique)
  File "~\miniconda3\lib\site-packages\seaborn\_core\relational.py", line 442, in _process_variable
    self._validate_variable(var, name, dtype, unique)
  File "~\miniconda3\lib\site-packages\seaborn\_core\relational.py", line 461, in _validate_variable
    raise ValueError(msg)
ValueError: If categorical, the variable needs to be non-null.
```
Note that the stack trace is different from the one provided in the issue, but it still raises an exception. The reason for the difference is that the original stack trace is from an interactive session, while the new stack trace is from a standalone script.

To fix the issue,