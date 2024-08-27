# mom6-plots
Centralized plotting styles and functions for MOM6 output

Many folks in the m2lines project are working with MOM6 ocean model output and might want to produce 'standardized' plots to evaluate e.g. the performance of different parametrizations against each other. 

This repository aims to provide 2 things:

- Consistent [Matplotlib Style Sheets](https://matplotlib.org/stable/users/explain/customizing.html#customizing-with-style-sheets), so that plots from different researchers can be combined in publications/presentations
- Common methods to compute reusable metrics (e.g. SST bias, OHC, ...) and plot them in a constistent way.

## Steps

### Prototype Plotting Functions

We will try to create plotting functions that adhere to the following structure:
```python
def plot_func(ds:xr.Dataset, ax:matplotlib.axes._axes.Axes=None, **kwargs) -> matplotlib.axes._axes.Axes:
    if ax is None:
        ax = plt.gca()
    ...
    return ax
```

The following requirements are given for the moment (subject to iteration and discussion):
- The function only ever produces a single pane/axis
- The input to the function is an xarray Dataset with an expected set of named dimensions/coordinates/data variables
- We use matplotlib for plotting.

### Working Dataset

Lets use this datasets (on the LEAP-Pangeo JupyterHub) to prototype plotting functions:
```python
# example output
import fsspec
import xarray as xr

zarr_data_path = 'gs://leap-persistent/jbusecke/ocean_emulators/OM4/OM4_raw_test.zarr'
nc_grid_path = 'gs://leap-persistent/sd5313/OM4-5daily/ocean_static_no_mask_table.nc'

ds_raw = xr.open_dataset(zarr_data_path, engine='zarr', chunks={})

with fsspec.open(nc_grid_path) as f:
    ds_grid = xr.open_dataset(f).load().drop_vars('time')
ds_grid = ds_grid.set_coords(ds_grid.data_vars)

# from https://github.com/m2lines/ocean_emulators/issues/17
dz = xr.DataArray(
    [
        5,
        10,
        15,
        20,
        30,
        50,
        70,
        100,
        150,
        200,
        250,
        300,
        400,
        500,
        600,
        800,
        1000,
        1000,
        1000,
    ],
    dims=["lev"],
)


ds = xr.merge([ds_raw, ds_grid]).assign_coords(dz=dz)
ds
```

## Next steps

- Prototype functions e.g. in a notebook during the hack
- Formalize plotting functions and make an installable package
- Test + Give feedback on various datasets on e.g. Greene



