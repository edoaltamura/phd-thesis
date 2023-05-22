"""
This script generates two plots related to the cosmology according to Planck 2018 results. The first plot illustrates 
the evolution of the density parameters, Omega_X, with redshift and scale-factor. The second plot shows the corresponding 
evolution of the Hubble parameter with the contributions of the individual components X. The values of the Omega_X and H(z=0) 
at the present day are indicated with markers. The Lambda, matter, and radiation eras are also indicated and separated by 
dashed grey lines.

LATEX Captions:
   \caption[Planck 2018 cosmology]{\textit{Top.} The evolution with redshift (and scale-factor) of the density 
   parameters $\Omega_X$ according to the \cite{2020A&A...641A...6P} cosmology. The values of the $\Omega_X$ at 
   the present day are indicated with markers on the left-hand-side. \textit{Bottom.} The corresponding evolution 
   of the Hubble parameter, with the contributions of the individual components $X$. The $\Lambda$, matter and 
   radiation eras are indicated in the top panel and they are separated by dashed grey lines. The value of $H(z=0) 
   \equiv H_0 = 67.66~{\rm km\,s}^{-1}\, {\rm Mpc}^{-1})$ is indicated with a marker, similarly to the plot above.}
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import transforms
from astropy import cosmology

# Use the MNRAS style for the plot
try:
    plt.style.use("mnras.mplstyle")
except:
    print(('Matplotlib stylesheet `mnras.mplstyle` not found. You can download it from ' 
           'https://github.com/edoaltamura/matplotlib-stylesheets - Reverting to default.'))

# Define the color palettes for reference and light
palette_ref = ["#ef476f", "#ffd166", "#06d6a0", "#118ab2", "#073b4c"]
palette_light = ["#ef476f", "#ffd166", "#06d6a0", "#118ab2", "#A768FF"]

# Calculate the scale factors for the plot
redshifts_p1 = np.logspace(0, 5, 100)
scale_factors = 1 / redshifts_p1

# Create the figure and axes
fig, axes = plt.subplots(2, 1, figsize=(3.1, 4.7), sharex=True, constrained_layout=True)

# Plot the density parameters evolution
ax = axes[0]
ax.loglog()

# Calculate and plot the total Omega
ax.plot(redshifts_p1, 
        cosmology.Planck18_arXiv_v2.Om(redshifts_p1 - 1) +
        cosmology.Planck18_arXiv_v2.Ogamma(redshifts_p1 - 1) +
        cosmology.Planck18_arXiv_v2.Ok(redshifts_p1 - 1) +
        cosmology.Planck18_arXiv_v2.Ode(redshifts_p1 - 1) +
        cosmology.Planck18_arXiv_v2.Onu(redshifts_p1 - 1), 
        color=palette_light[3],
        label=r'$\Omega = \Omega_{m} + \Omega_{r} + \Omega_{k} + \Omega_{\Lambda} + \Omega_{\nu}$')

# Calculate and plot the individual Omegas
ax.plot(redshifts_p1, cosmology.Planck18_arXiv_v2.Ob(redshifts_p1 - 1), label=r'$\Omega_{b}$  Baryons', color=palette_ref[0], lw=0.8, ls=':')
ax.plot(redshifts_p1, cosmology.Planck18_arXiv_v2.Odm(redshifts_p1 - 1), label=r'$\Omega_{\rm CDM}$  Cold dark matter', color=palette_ref[0], lw=0.8, ls='--')
ax.plot(redshifts_p1, cosmology.Planck18_arXiv_v2.Om(redshifts_p1 - 1), label=r'$\Omega_{m}$  Matter (CDM + baryons)', color=palette_ref[0])
ax.plot(redshifts_p1, cosmology.Planck18_arXiv_v2.Ogamma(redshifts_p1 - 1), label=r'$\Omega_{r}$  Radiation', color=palette_ref[1])
ax.plot(redshifts_p1, cosmology.Planck18_arXiv_v2.Ok(redshifts_p1 - 1), label=r'$\Omega_{k}$  Curvature', color=palette_ref[2])
ax.plot(redshifts_p1, cosmology.Planck18_arXiv_v2.Ode(redshifts_p1 - 1), label=r'$\Omega_{\Lambda}$  Dark energy', color=palette_ref[4])
ax.plot(redshifts_p1, cosmology.Planck18_arXiv_v2.Onu(redshifts_p1 - 1), label=r'$\Omega_{\nu}$  Neutrinos', color=palette_light[4])

# Indicate the values of the Omegas at the present day
ax.scatter([1], [cosmology.Planck18_arXiv_v2.Ob0], s=3, color=palette_light[0])
ax.scatter([1], [cosmology.Planck18_arXiv_v2.Odm0], s=3, color=palette_light[0])
ax.scatter([1], [cosmology.Planck18_arXiv_v2.Om0], s=7, color=palette_ref[0])
ax.scatter([1], [cosmology.Planck18_arXiv_v2.Ogamma0], s=7, color=palette_ref[1])
ax.scatter([1], [cosmology.Planck18_arXiv_v2.Ok0], s=7, color=palette_ref[2])
ax.scatter([1], [cosmology.Planck18_arXiv_v2.Ode0], s=7, color=palette_ref[4])
ax.scatter([1], [cosmology.Planck18_arXiv_v2.Onu0], s=7, color=palette_light[4])

trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)

ax.text(2.5, 0.05, 
        r'$\Omega_{k} = 0$',
        horizontalalignment='left',
        verticalalignment='bottom',
        color=palette_ref[2],
        rotation=0,
        transform=trans,
        zorder=100,
        fontsize=8)

# Set the x-axis limit and labels
ax.legend(facecolor='w', edgecolor='none', framealpha=0.9, frameon=True)
ax.set_ylim(1e-5, 2)
ax.set_ylabel(r'$\Omega_X$')
ax.grid(ls='--', c='grey', lw=0.5, alpha=0.3)

ax2 = ax.twiny()
ax2.set_xscale('log')
ax2.set_xlim(1 / 0.3, 1e-5)
ax2.set_xlabel('Scale-factor')

# Plot the Hubble parameter evolution
ax = axes[1]
ax.loglog()

# Calculate and plot the total Hubble parameter and its components
ax.plot(redshifts_p1, cosmology.Planck18_arXiv_v2.H(redshifts_p1 - 1), color = palette_light[3], lw=2, zorder=0)
ax.plot(redshifts_p1, cosmology.Planck18_arXiv_v2.H0 * np.sqrt(cosmology.Planck18_arXiv_v2.Om0 * scale_factors ** -3), color=palette_ref[0], zorder=0)
ax.plot(redshifts_p1, cosmology.Planck18_arXiv_v2.H0 * np.sqrt(cosmology.Planck18_arXiv_v2.Ob0 * scale_factors ** -3), color=palette_ref[0], lw=0.8, ls=':', zorder=0)
ax.plot(redshifts_p1, cosmology.Planck18_arXiv_v2.H0 * np.sqrt(cosmology.Planck18_arXiv_v2.Odm0 * scale_factors ** -3), color=palette_ref[0], lw=0.8, ls='--', zorder=0)
ax.plot(redshifts_p1, cosmology.Planck18_arXiv_v2.H0 * np.sqrt(cosmology.Planck18_arXiv_v2.Ogamma0 * scale_factors ** -4), color=palette_ref[1], zorder=0)
ax.plot(redshifts_p1, cosmology.Planck18_arXiv_v2.H0 * np.sqrt(cosmology.Planck18_arXiv_v2.Ok0 * scale_factors ** -2), color=palette_ref[2], zorder=0)
ax.plot(redshifts_p1, cosmology.Planck18_arXiv_v2.H0 * np.sqrt(cosmology.Planck18_arXiv_v2.Ode0) * np.ones_like(scale_factors), color=palette_ref[4], zorder=0)

# Indicate the value of H(z=0)
ax.scatter([1], [cosmology.Planck18_arXiv_v2.H0.value], s=15, edgecolor='grey', linewidth=0.2, facecolor=palette_light[3])

ax.text(0.5, cosmology.Planck18_arXiv_v2.H0.value, 
        r'$H_0$',
        horizontalalignment='center',
        verticalalignment='center',
        color='k',
        rotation=0,
        transform=ax.transData,
        zorder=100,
        fontsize=8)

# Set the x-axis and y-axis limits and labels
ax.set_ylabel(r'$H(z)$  [km s$^{-1}$ Mpc$^{-1}$]')
ax.set_xlabel(r'$z+1$')
ax.grid(ls='--', c='grey', lw=0.5, alpha=0.3)
ax.set_ylim(10, 1e9)
ax.set_xlim(0.3, 1e5)

# Indicate the eras and their equalities
matter_radiation_equality = cosmology.Planck18_arXiv_v2.Ogamma0 / cosmology.Planck18_arXiv_v2.Om0
ax.axvline(1 / matter_radiation_equality, color='grey', ls='--')
axes[0].axvline(1 / matter_radiation_equality, color='grey', ls='--')

matter_lambda_equality = (cosmology.Planck18_arXiv_v2.Om0 / cosmology.Planck18_arXiv_v2.Ode0) ** (1 / 3)
ax.axvline(1 / matter_lambda_equality, color='grey', ls='--')
axes[0].axvline(1 / matter_lambda_equality, color='grey', ls='--')

ax.axvspan(ax.get_xlim()[1], 1 / matter_radiation_equality, ymin=0.925, ymax=1., color=palette_ref[1])
ax.axvspan(1 / matter_radiation_equality, 1 / matter_lambda_equality, ymin=0.925, ymax=1., color=palette_ref[0])
ax.axvspan(1 / matter_lambda_equality, ax.get_xlim()[0], ymin=0.925, ymax=1., color=palette_ref[4])

# Generate dictionary for common properties
trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
eras_label_kwargs = dict(horizontalalignment='left', verticalalignment='center', 
                         transform=trans, zorder=100, fontsize=8)

ax.text(8e3, 0.95, r'Radiation', color='k', rotation=0, **eras_label_kwargs)
ax.text(50, 0.95, r'Matter', color='k', rotation=0, **eras_label_kwargs)
ax.text(0.5, 0.95, r'$\Lambda$', color='w', rotation=0, **eras_label_kwargs)
ax.text(1 / matter_radiation_equality * 1.1, 0.4, '$(m-r)$ equality', color='k', rotation=90, **eras_label_kwargs)
ax.text(1 / matter_lambda_equality * 1.1, 0.6, '$(m-\Lambda)$ equality', color='k', rotation=90, **eras_label_kwargs)

# Save and display the figure
plt.savefig('cosmological_parameters.pdf')
