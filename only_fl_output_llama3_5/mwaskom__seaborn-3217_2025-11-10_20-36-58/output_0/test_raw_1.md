Here is the reproducer script:

```python
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool
import so

def main():
    tips = pd.read_csv('tips.csv')

    p = figure(title="Total Bill", x_axis_label='total_bill', y_axis_label='Count')
    
    bars = p.vbar(x=[x for x in tips['total_bill']], 
                 width=1, 
                 bottom=0, 
                 height=[y for y in tips['total_bill'].value_counts()], 
                 fill_color='blue', 
                 line_width=0, 
                 alpha=0.3)
    
    p.hist([tips['total_bill']], 
           bins=4, 
           orientation='horizontal', 
           color='blue')
    
    output_file('reproducer.html')
    show(p)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```

This script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.

Please note that you need to have bokeh, pandas and so libraries installed in your Python environment for this script to run correctly.