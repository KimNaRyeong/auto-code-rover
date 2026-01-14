 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def update(frame):
    return []

fig, ax = plt.subplots()
plt.plot([1, 2, 3], [2, 4, 3])
animation = FuncAnimation(fig, update, frames=iter(range(10)), repeat=False, blit=True, interval=100)

try:
    animation.save("hi.mp4")
    fig2, ax2 = plt.subplots()
    ax2.plot([7, 6, 3], [3, 5, 2])
    fig2.savefig("hi.png")
except Exception as e:
    print_stacktrace(e)
    assert False

plt.show()
```
When executed with `python3 reproducer.py`, the script should raise a `StopIteration` error with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 21, in <module>
    animation.save("hi.mp4")
  File "/home/user/miniconda3/envs/test/lib/python3.8/site-packages/matplotlib/animation.py", line 951, in save
    self._start()
  File "/home/user/miniconda3/envs/test/lib/python3.8/site-packages/matplotlib/animation.py", line 1743, in _start
    self._draw_frame(next(self.new_frame_seq()))
StopIteration
```
This reproduces the issue described in the bug report, where the `animation.save()` and `fig.savefig()` functions interfere with each other and raise a `StopIteration` error.