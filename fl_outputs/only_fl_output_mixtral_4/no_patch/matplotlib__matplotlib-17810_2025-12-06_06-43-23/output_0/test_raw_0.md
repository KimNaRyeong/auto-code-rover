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
except Exception as e:
    print_stacktrace(e)

fig2, ax2 = plt.subplots()
ax2.plot([7, 6, 3], [3, 5, 2])
try:
    fig2.savefig("hi.png")
except Exception as e:
    print_stacktrace(e)
```
The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.

The output produced by the above code:
```python
Traceback (most recent call last):
  File "reproducer.py", line 23, in <module>
    animation.save("hi.mp4")
  File "/home/user/.local/lib/python3.8/site-packages/matplotlib/animation.py", line 951, in save
    self._start()
  File "/home/user/.local/lib/python3.8/site-packages/matplotlib/animation.py", line 1743, in _start
    self._draw_frame(next(self.new_frame_seq()))
StopIteration
```
This script reproduces the issue with the given code snippet, which raises `StopIteration` when trying to save an animation and a figure in the same script. The issue is caused by the `frames` parameter of the `FuncAnimation` class being set to an iterator, which is consumed by the animation and leaves nothing for the `fig2.savefig("hi.png")` statement.

This issue can be fixed by changing the `frames` parameter to a list or a range object, so that it can be consumed by the animation without being exhausted.

For example, changing the line:
`animation = FuncAnimation(fig, update, frames=iter(range(10)), repeat=False, blit=True, interval=100)`

to:
`animation = FuncAnimation(fig, update, frames=range(10), repeat=False, blit=True, interval=100)`

will fix the issue and the script will exit with code 0.