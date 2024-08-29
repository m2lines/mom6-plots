import warnings
import cartopy
import cartopy.crs as ccrs
import xarray as xr
import matplotlib
import matplotlib.pyplot as plt


rename_dict = {
    'xh':'x',
    'yh':'y',
    'geolon':'lon',
    'geolat':'lat',
}

def default_decorator(func, logo=True):
    def all_plot_defaults(*args, **kwargs):
        # TODO: Check that all positional arguments are dataarrays and that they are consistent?
        checked_args = []
        for da in args:
            # check that input is dataarray (what of this can I refactor to an xarray-schema?)
            if not isinstance(da, xr.DataArray):
                raise ValueError(f'Input to plotting function can only be an xr.DataArray. Got {type(da)}')
        
            # attempt to rename according to known renaming scheme
            all_coords_dims = set(list(da.coords) + list(da.dims))
            da = da.rename({k:v for k,v in rename_dict.items() if k in all_coords_dims})
            checked_args.append(da)
        
        if kwargs.get('ax') is None: #FIXME: This does not work well when passing ax as positional argument. Gives 'multiple ax...' error
            warnings.warn('No `ax` input provided. Using the current axis.')
            kwargs['ax'] = plt.gca()
        
        logo = kwargs.pop('logo', None)
        
        ax = func(*checked_args, **kwargs)
        
        if logo:
            ax.text(
                -0.1,
                -0.2,
                'Made with ❤️ at m2lines', 
                horizontalalignment='left',
                verticalalignment='bottom',
                transform=ax.transAxes,
                fontsize=10
            )
        return ax
    return all_plot_defaults


def decorator_2d(func):
    def checks_2d(*args, **kwargs):
        # 2d plots cannot have more than one dataarray as input
        if len(args) != 1:
            raise ValueError(f'{func} takes exactly one positional argument. Got {len(args)}:{args}')
        else:
            da = args[0]

        if not len(da.dims) == 2:
            raise ValueError(f"Can only plot data arrays with two dimensions. Got {da.dims}")
        return func(*args, **kwargs)

    return checks_2d

def timeseries_decorator(func):
    def checks_1d(*args, **kwargs):
        # 2d plots cannot have more than one dataarray as input
        for da in args:
            if not len(da.dims) == 1:
                raise ValueError(f"Can only plot data arrays with one dimensions. Got {da.dims}")
        return func(*args, **kwargs)

    return checks_1d

def map_decorator(func):
    def cartopy_inner(*args, **kwargs):
        # checks the axis and adds common elements (land, coastlines) to cartopy plots

        # TODO: More strict check of the coordinates here (otherwise they will fail below with less clear error).
        
        
        if not isinstance(kwargs['ax'], cartopy.mpl.geoaxes.GeoAxes):
            raise ValueError("Axis has to be `cartopy.mpl.geoaxes.GeoAxes`. Pass `projection=ccrs.<some_projection>` to the axis creation.")
            #TODO: Can we automatically replace the axis with a new one?
        
        ax = func(*args, **kwargs)

        ax.add_feature(cartopy.feature.COASTLINE, color='0.3', facecolor='0.2')
        return ax
        
    return cartopy_inner

@map_decorator
@decorator_2d
@default_decorator
def map_plot(da, ax=None, **kwargs):
    """Plots a map of the data in `da` to `ax`. `kwargs` are passed to xarray.plot()"""
    kwargs.setdefault('x','lon')
    kwargs.setdefault('y', 'lat')
    da.plot(
        ax=ax,
        transform=ccrs.PlateCarree(),
        **kwargs
    )
    return ax

@decorator_2d
@default_decorator
def section_plot(da, ax=None, **kwargs):
    raise NotImplementedError

@decorator_2d
@default_decorator
def hovmoeller_plot(da, ax=None, **kwargs):
    raise NotImplementedError

@timeseries_decorator
@default_decorator
def timeseries_plot(*args, ax=None, labels=None, **kwargs):
    kwargs.setdefault('x','time')
    # parse labels
    if not labels:
        labels = [None for da in args]
    else:
        if len(labels) != len(args):
            raise ValueError(f"If labels are provided there must be one label per input array. Got {len(args)} arrays and {len(labels)} labels")
    for da,l in zip(args, labels):
        da.plot(ax=ax, label=l,**kwargs)
    ax.legend()
    return ax