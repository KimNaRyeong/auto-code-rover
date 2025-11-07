import xarray as xr
import numpy as np

def reproduce_issue():
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    try:
        ds.coarsen(time=12).construct(time=("year", "month"))
        assert False, "Expected an AssertionError"
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
