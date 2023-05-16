"""
Generates a diagram of the horizon crossing of cosmological perturbations
at early times. The scales of momentum and wavenumber are in natural units.
See /images for the example output.

LATEX Caption:
  \caption[Horizon-crossing]{Evolution of the comoving momentum $q$ with 
  scale-factor $a$ for three different scalar modes (wavelength $\lambda = $1 
  Mpc, 100 Mpc, 1 Gpc) crossing the horizon, indicated by the Hubble parameter 
  $H(a)$ \citep{2020A&A...641A...6P}. We indicate the horizon-crossing scale 
  factors with markers, assuming linear growth across the entire domain. 
  Smaller perturbations enter the horizon at earlier times than larger-wavelength 
  modes. Instead, the larger 30 Gpc mode (purple) never crosses the horizon 
  for $a<1$.}
"""

import numpy as np
from matplotlib import pyplot as plt
from astropy import cosmology
import scipy.constants as const

def get_aspect(ax):
    """
    Calculate the aspect ratio of the given axes.
    
    :param ax: Matplotlib axes object
    :return: Aspect ratio of the axes
    """
    # Get total figure size
    figW, figH = ax.get_figure().get_size_inches()

    # Get axis size on figure
    _, _, w, h = ax.get_position().bounds

    # Calculate ratio of display units
    disp_ratio = (figH * h) / (figW * w)

    # Calculate ratio of data units
    # Note: Negative over negative due to the order of subtraction
    delta_y =  np.log10(ax.get_ylim()[1]) - np.log10(ax.get_ylim()[0]) if ax.get_yscale() == 'log' else sub(*ax.get_ylim())
    delta_x =  np.log10(ax.get_xlim()[1]) - np.log10(ax.get_xlim()[0]) if ax.get_xscale() == 'log' else sub(*ax.get_xlim())
    
    data_ratio = delta_y / delta_x

    return disp_ratio / data_ratio


def mode(wavelength_mpc):
    """
    Calculate the mode of the given wavelength in Mpc.

    :param wavelength_mpc: Wavelength in Mpc
    :return: Mode of the wavelength
    """
    mode_conversion = const.parsec * 1e6
    return 4 * np.pi / (wavelength_mpc * mode_conversion)

  
# Use the MNRAS style for the plot
try:
    plt.style.use("mnras.mplstyle")
else:
    print(('Matplotlib stylesheet `mnras.mplstyle` not found. You can download it from ' 
           'https://github.com/edoaltamura/matplotlib-stylesheets - Reverting to default.'))

# Define color palette
palette_ref = ["#ef476f","#ffd166","#06d6a0","#A768FF"]

# Define redshifts and scale factors
redshifts_p1 = np.logspace(0, 9, 100)
scale_factors = 1 / redshifts_p1

# Calculate natural frequency in Hz
Hz_natural = cosmology.Planck18_arXiv_v2.H(redshifts_p1) * 1000 / const.parsec / const.year / 1e6

# Create figure and axes
fig, ax = plt.subplots()

ax.loglog()
ax.plot(scale_factors, Hz_natural, label='$H(a)$')

for i, (l, txt) in enumerate(zip([1, 100, 1000, 30000], 
                                 ["1 Mpc", "100 Mpc", "1 Gpc", "30 Gpc"])):
    ax.plot(scale_factors, mode(l) / scale_factors, label=f'$q(a,\, \lambda =$ {txt})', color=palette_ref[i])
    
    x_cross_id = np.argmin(np.abs(np.log(mode(l) / scale_factors) - np.log(Hz_natural.value)))
    x_cross = scale_factors[x_cross_id]
    y_cross = mode(l) / x_cross
    ax.scatter(x_cross, y_cross,  color=palette_ref[i], zorder=10)
    
    if l == 1:
        plt.annotate('Horizon crossing', xy=(x_cross * 1.05, y_cross * 1.05), 
                     xytext=(x_cross, y_cross * 1e3), 
                     horizontalalignment='left',
                     verticalalignment='center',
                     color='k',
                     zorder=100,
                     fontsize=8, 
                     arrowprops=dict(arrowstyle="->", mutation_scale=10))

ax.set_ylabel(r'$q(a)\qquad$ [Mpc$^{-1}$]')
ax.set_xlabel('Scale-factor')
ax.legend(frameon=True, facecolor='w', edgecolor='none')
ax.grid(ls='--', c='grey', lw=0.5, alpha=0.3)
ax.set_ylim(1e-25, 1e-12)
ax.set_xlim(1e-8, 1)

# Define common kwargs and properties
text_kwargs = dict(color='k', zorder=100)
arrow_kwargs = dict(arrowstyle="->", mutation_scale=10)
rotation_angle = np.arctan(-get_aspect(ax)) / np.pi * 195

plt.annotate('Super-horizon', 
             xytext=(3e-7, mode(10) / 3e-7), 
             xy=(1e-3, mode(10) / 1e-3), 
             horizontalalignment='center',
             verticalalignment='center',
             rotation=rotation_angle,
             fontsize=8, 
             arrowprops=dict(ls='--', **arrow_kwargs),
             **text_kwargs)

plt.annotate('Sub-horizon', 
             xy=(1e-7, mode(10) / 1e-7), 
             xytext=(8e-3, mode(10) / 8e-3), 
             horizontalalignment='center',
             verticalalignment='center',
             rotation=rotation_angle,
             fontsize=8
             **text_kwargs))

plt.annotate('No horizon crossing in the past', 
             xytext=(3e-7, mode(2.8e5) / 3e-7), 
             xy=(1e-3, mode(2.8e5) / 1e-3), 
             horizontalalignment='center',
             verticalalignment='bottom',
             rotation=rotation_angle,
             fontsize=5,
             **text_kwargs))

plt.annotate('Early times', 
             xy=(3e-8, 1e-24), 
             xytext=(3e-7, 1e-24), 
             horizontalalignment='left', 
             verticalalignment='center',
             fontsize=8,
             arrowprops=dict(ls='-', **arrow_kwargs),
             **text_kwargs))

plt.annotate('Late times', 
             xy=(3e-2, 1e-24), 
             xytext=(3e-3, 1e-24), 
             horizontalalignment='right', verticalalignment='center',
             fontsize=8,
             arrowprops=dict(ls='-', **arrow_kwargs),
             **text_kwargs))

# Save the final figure
plt.savefig('cosmological_horizon.pdf')
