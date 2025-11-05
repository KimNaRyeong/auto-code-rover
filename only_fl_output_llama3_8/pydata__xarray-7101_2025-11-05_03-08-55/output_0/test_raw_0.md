Here is the reproducer script:

```Python
import xarray as xr
import unittest
from io import StringIO

def test_assign_coords_drop_coord_names(self) -> None:
    ds = xr.DataArray(
        [[[1, 1], [0, 0]], [[2, 2], [1, 1]]],
        dims=("lat", "year", "month"),
        coords={"lat": [-60, 60], "year": [2010, 2020], "month": [3, 6]},
        name="test",
    ).to_dataset()

    stacked = ds.stack(time=("year", "month"))
    stacked = stacked.assign_coords(
        {"time": [y + m / 12 for y, m in stacked["time"].values]}
    )

    try:
        len(stacked)
        print(stacked)
    except ValueError as e:
        print_stacktrace(e)

class TestAssignCoords(unittest.TestCase):
    def test_assign_coords_drop_coord_names(self) -> None:
        test_assign_coords_drop_coord_names(None)

if __name__ == "__main__":
    unittest.main()
```

To run the script, you can execute `python3 reproducer.py` in your terminal.