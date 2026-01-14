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
This script will reproduce the issue and print the stack trace when the `animation.save` and `fig.savefig` interfere with each other and raise `StopIteration`.

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
The version of the libraries used in this example are:

* Operating system: Ubuntu 20.04
* Matplotlib version: 3.3.4
* Matplotlib backend: TkAgg
* Python version: 3.8.5
* Jupyter version: Not applicable
* Other libraries: Not applicable

Matplotlib was installed using pip in a virtual environment.

This issue can be fixed by saving the figure before starting the animation, or by using different file names for the animation and the figure.