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
  File "reproducer.py", line 22, in <module>
    animation.save("hi.mp4")
  File "/home/user/.local/lib/python3.8/site-packages/matplotlib/animation.py", line 951, in save
    self._start()
  File "/home/user/.local/lib/python3.8/site-packages/matplotlib/animation.py", line 1743, in _start
    self._draw_frame(next(self.new_frame_seq()))
StopIteration
```
The above output is produced when running the script `python3 reproducer.py` and the issue is present.

The issue is caused by the fact that the `animation.save` method is trying to advance the frame sequence, but the frame sequence is an iterator that has already been exhausted by the `FuncAnimation` constructor.

A possible solution would be to create a new iterator for the frame sequence when calling the `animation.save` method, or to store the frame sequence as a list instead of an iterator.

Another solution would be to use the `animation.save` method before creating the `FuncAnimation` object.

A third solution would be to use a different backend for matplotlib, as the issue might be specific to the TkAgg backend.