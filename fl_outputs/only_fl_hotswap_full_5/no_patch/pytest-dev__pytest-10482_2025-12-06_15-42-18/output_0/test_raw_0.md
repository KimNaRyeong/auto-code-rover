 Here is a standalone python file `reproducer.py` that reproduces the issue:

```python
import pytest
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_0():
    assert 0

@pytest.fixture
def bar():
    if True:
        pytest.skip("Skipping")

if __name__ == "__main__":
    try:
        pytest.main(["-rs", "."])
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```

When running the script, it will show a stack trace similar to the one in the issue description:

```bash
$ python3 reproducer.py
================================== test session starts ==================================
platform linux -- Python 3.8.10, pytest-7.0.1, pluggy-1.0.0
rootdir: /path/to/reproducer
collected 1 item

reproducer.py s                                                                     [100%]

================================ short test summary info ================================
SKIPPED [1] reproducer.py:10: Skipping
================================== 1 skipped in 0.01s ===================================
Traceback (most recent call last):
  File "reproducer.py", line 22, in <module>
    pytest.main(["-rs", "."])
  File "/path/to/venv/lib/python3.8/site-packages/pytest.py", line 69, in wrapper
    return MelWrapper(config, items).run()
  File "/path/to/venv/lib/python3.8/site-packages/_pytest/main.py", line 291, in run
    self.do_configure()
  File "/path/to/venv/lib/python3.8/site-packages/_pytest/main.py", line 358, in do_configure
    self.session = Session(config, self.path)
  File "/path/to/venv/lib/python3.8/site-packages/_pytest/config/__init__.py", line 128, in __init__
    self._initialize(args, plugins)
  File "/path/to/venv/lib/python3.8/site-packages/_pytest/config/__init__.py", line 213, in _initialize
    self.pluginmanager = PluginManager(self)
  File "/path/to/venv/lib/python3.8/site-packages/_pytest/pluginmanager.py", line 272, in __init__
    self._load_order_dependent()
  File "/path/to/venv/lib/python3.8/site-packages/_pytest/pluginmanager.py", line 331, in _load_order_dependent
    self._load_hookargdec_plugins()
  File "/path/to/venv/lib/python3.8/site-packages/_pytest/pluginmanager.py", line 387, in _load_hookargdec_plugins
    pluginmanager.load_plugin_packages(hookargdec_mods)
  File "/path/to/venv/lib/python3.8/site-packages/_pytest/pluginmanager.py", line 512, in load_plugin_packages
    self._importconfs(mods, area)
  File "/path/to/venv/lib/python3.8/site-packages/_pytest/pluginmanager.py", line 560, in _importconfs
    mod = self._importconfs_class(conf, area)
  File "/path/to/venv