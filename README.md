# mom6-plots
Centralized plotting styles and functions for MOM6 output

Many folks in the m2lines project are working with MOM6 ocean model output and might want to produce 'standardized' plots to evaluate e.g. the performance of different parametrizations against each other. 

This repository aims to provide 2 components to make it easier for m2lines members to produce plots for model evaluation:

- Standardized plotting functions and consistent [Matplotlib Style Sheets](https://matplotlib.org/stable/users/explain/customizing.html#customizing-with-style-sheets), so that plots from different researchers can be combined in publications/presentations.
- Common methods to compute reusable metrics (e.g. SST bias, OHC, ...) to enable direct comparison between different researchers.

## Installation

You can install this package via pip by either:

- Checking the repository out locally (recommended if you want to contribute/edit) and from the root directory of your local repository do:
```
pip install -e .
```

- Installing the current main branch from github (faster version if you just want to use the plotting functions):
```
pip install git+https://github.com/m2lines/mom6-plots.git
```

## Standardized Plotting

We provide 4 types of *base plot* functions:
- A map plot (`mom6_plots.base_plots.map`)
- A timeseries plot (`mom6_plots.base_plots.timeseries`)
- Coming Soon: A vertical section plot
- Coming Soon: A Hovmoeller plot

Each of these functions takes one or multiple (timeseries only) [xarray.DataArrays](https://docs.xarray.dev/en/stable/getting-started-guide/why-xarray.html#core-data-structures) as positional input. The plotting is based on the [xarray plotting](https://docs.xarray.dev/en/stable/user-guide/plotting.html). We attempt renaming dimensions and coordinates for known variants of MOM6 data. If you find that your particular naming convention causes issues, please [raise an isseu](https://github.com/m2lines/mom6-plots/issues).

If you have suggestions how to improve the look of each of these plots (e.g. different color, linewidth, etc), please start a discussion by [raising an issue](https://github.com/m2lines/mom6-plots/issues). Our aim here is to have a standardized plotting style that hopefully can reflect most folks preferences in the project.

Each plotting function consumes and returns a matplotlib axis, if no axis is provided they will call `matplotlib.pyplot.gca`.

You can find examples of how to use these functions in the [demo notebook](./notebooks/base_plot_demo.ipynb).

## Common methods to compute metrics

This is a much broader topic. In order to make progress I encourage everyone to submit example notebooks (ideally using upstream packages/examples to avoid duplication) as PRs so we can gather an overview of how/what folks acrosse the project think would be useful to add here. Ideally try to use the dataset below on the LEAP-Pangeo Jupyterhub to make things easily testable.
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
