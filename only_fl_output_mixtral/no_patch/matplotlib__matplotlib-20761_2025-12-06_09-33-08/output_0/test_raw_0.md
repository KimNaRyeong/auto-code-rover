 Here is a standalone python script `reproducer.py` that reproduces the issue:
```python
import matplotlib.pyplot as plt

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

fig = plt.figure(constrained_layout=True, figsize=(10, 8))

# create top/bottom subfigs
# see https://stackoverflow.com/a/68553015/9249533
(subfig_t, subfig_b) = fig.subfigures(2, 1, hspace=0.05, height_ratios=[1, 3])

# put ax0 in top subfig
ax0 = subfig_t.subplots()

# create left/right subfigs nested in bottom subfig
(subfig_bl, subfig_br) = subfig_b.subfigures(1, 2, wspace=0.1, width_ratios=[3, 1])

# put ax1-ax3 in gridspec of bottom-left subfig
gs = subfig_bl.add_gridspec(nrows=1, ncols=9)

ax1 = subfig_bl.add_subplot(gs[0, :3])
ax2 = subfig_bl.add_subplot(gs[0, 3:6], sharey=ax1)
ax3 = subfig_bl.add_subplot(gs[0, 6:9], sharey=ax1)

ax1.set_title('Nov. 7 to Nov. 13')
ax2.set_title('Nov. 13 to Nov. 27')
ax3.set_title('Nov. 27 to Dec. 31')
ax2.get_yaxis().set_visible(False)
ax3.get_yaxis().set_visible(False)

subfig_bl.supxlabel("My Subfigure Label", x=0.54, size=12, fontweight='bold')

# put ax4 in bottom-right subfig
ax4 = subfig_br.subplots()
ax4.set_title('Some Other Title')

try:
    # add 'x' kwarg to supxlabel
    subfig_br.supxlabel('Other Subfigure SubLabel', x=0.5, size=12, fontweight='bold')
except Exception as e:
    print_stacktrace(e)
    assert False

plt.show()
```
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 35, in <module>
    subfig_br.supxlabel('Other Subfigure SubLabel', x=0.5, size=12, fontweight='bold')
  File "/Users/username/miniforge3/envs/myenv/lib/python3.9/site-packages/matplotlib/figure.py", line 1866, in supxlabel
    return self.text(0.5, 1.02, s, transform=self.transFigure,
  File "/Users/username/miniforge3/envs/myenv/lib/python3.9/site-packages/matplotlib/text.py", line 270, in __init__
    bbox_artist = self.draw(renderer)
  File "/Users/username/miniforge3/envs/myenv/lib/python3.9/site-packages/matplotlib/text.py", line 1002, in draw
    bbox, info, descent =