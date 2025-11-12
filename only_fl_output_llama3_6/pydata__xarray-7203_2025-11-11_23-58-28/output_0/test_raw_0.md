Here is the reproducer script:

```Python
import xarray as xr
import os
import time

# Create a test dataset with 48 "small" variables
dc1 = xr.open_dataset('s3://its-live-data/datacubes/v02/N40E080/ITS_LIVE_vel_EPSG32645_G0120_X250000_Y4750000.zarr', engine='zarr', storage_options={'anon': True})

# Measure the time it takes to display the repr
start_time = time.time()
dc1._repr_html_()
end_time = time.time()

# Check if the time taken is more than 36.4 seconds (the expected time)
if end_time - start_time > 36.4:
    print("AssertionError: Repr took too long!")
    raise AssertionError
else:
    print(f"Repr took {end_time - start_time} seconds, which is within the expected time.")
```

This script creates a test dataset with 48 "small" variables and measures the time it takes to display its repr. If the time taken is more than 36.4 seconds (the expected time), it raises an `AssertionError`.