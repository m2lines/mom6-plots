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

## Next steps

- Prototype functions e.g. in a notebook during the hack
- Formalize plotting functions and make an installable package
- Test + Give feedback on various datasets on e.g. Greene



