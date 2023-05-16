"""
Python script for generating the disk usage at different stages of the zoom-in simulation project.
This script produces a plot of the disk usage, with the x-axis showing the usage in bytes and the 
y-axis showing the processes numbered sequentially. The processes are color-coded according to 
the category they fall into, and the filled markers represent the disk usage for each specific 
process while the empty markers represent the cumulative usage. The vertical lines indicate common 
file sizes used by the human-readable format.

LATEX Caption:
  \caption{Disk usage at different stages of the zoom-in simulation project in chapters 
  \ref{chapter:5} and \ref{chapter:6}. The usage, in bytes, is shown in the $x$-axis and 
  the processes are numbered sequentially, as indicated in the $y$-axis. The pipeline 
  starts at the top (0) and ends at bottom (14). We divide the simulation steps into four 
  categories: parent simulation (red), the object selection and zoom-in simulation set-up 
  (yellow), the simulation model calibration (green) and the final analysis (purple). The 
  filled markers indicate the disk usage for each specific process, and the empty markers 
  are the cumulative usage. The vertical lines indicate common file sizes used by the 
  human-readable format.}
"""

import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt
from matplotlib import transforms
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# Use the MNRAS style for the plot
try:
    plt.style.use("mnras.mplstyle")
else:
    print(('Matplotlib stylesheet `mnras.mplstyle` not found. You can download it from ' 
           'https://github.com/edoaltamura/matplotlib-stylesheets - Reverting to default.'))

# Color palette to be used in the plot
palette_ref = ["#ef476f", "#ffd166", "#06d6a0", "#A768FF"]


def convert_bytes(num: int, unit_only: bool = False) -> str:
    """
    Converts bytes to human-readable format.
    
    Parameters
    ----------
    num : int
        The number of bytes.
    unit_only : bool, optional
        If True, returns only the unit of the byte size. Default is False.
        
    Returns
    -------
    str
        The byte size in a human-readable format.
    """
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if num < 1024.0:
            if unit_only:
                return unit
            return f"{num:3.1f} {unit}"
        num /= 1024.0

# Define colors for each process category
colors = ["#ef476f"] * 6 + ["#ffd166"] * 5 +  ["#06d6a0"] * 2 + ["#A768FF"] * 2

# Define labels for each process
label = [
    # Parent simulation
    "Panphasian descriptor\n+ cosmology",
    "Panphasia inputs",
    "Glass file",
    "Initial conditions",
    "Snapshots",
    "Halo catalogues",
    
    # Object selection and zoom-in simulation set-up
    "Object selection",
    "Zoom mask",
    "Zoom initial conditions",
    "Snapshots DMO",
    "Halo catalogues DMO",    
    
    # Simulation model calibration
    "Sub-grid calibration",
    "Fiducial simulation",
    
    # Final analysis
    "Data products",
    "Plots & insights"    
]

byte_size = np.asarray(byte_size)
process_id = np.arange(len(byte_size))

# Define byte size for each process
# The size is in bytes
byte_size = [
    69 + 6*4 + 7*16,
    44,
    2948 * 1024, 
    4339072582 * 1024,
    285253668 * 1024,
    20303636 * 1024,
    
    30 * 4,
    6604 * 1024,
    747403724 * 1024,
    573958792 * 1024,
    154754024 * 1024,
    
    (27711872475 + 24796451415 + 19728229448) * 1024 + 9 * 1024 ** 4,
    45859195689 * 1024,
    
    437 * 1024,
    47 * 1024,
]

# Start of the plotting process
# Create the figure and axes
fig, axes = plt.subplots(figsize=(3.8, 5))
axes.set_xscale('log')
axes.invert_yaxis()
axes.set_yticks(process_id)
axes.set_xticks([10 ** (i * 2 - 1) for i in range(1, 9)])
axes.xaxis.tick_top()
axes.xaxis.set_label_position('top')

# Define the bar plot parameters
bar_kwargs = dict(height=0.1, align='center', alpha=1, tick_label=[''], zorder=2)

# Plot each process and its disk usage
x_cumsum = 0
for y, x, c, l in zip(process_id, byte_size, colors, label):
    x_cumsum += x
    axes.scatter(x_cumsum, y, edgecolor=c, alpha=1, facecolor='white', s=40, zorder=7)
    axes.plot([1, 1E15], [y, y], color=c, alpha=0.75, linestyle=":", linewidth=0.8, zorder=6)
    
    axes.scatter(x, y, facecolor=c, edgecolor='none', s=20, zorder=8)
    axes.plot([1, x], [y, y], color=c, linestyle="-", linewidth=1.5, zorder=9)
    axes.text(2E15, y, l, fontsize=6, va='center')

# Draw the lines and text indicating the common file sizes in human-readable format    
for i in range(1, 6):
    axes.axvline(1024 ** i, color='grey', linestyle='--', linewidth=0.75)
    axes.text(1024 ** i * 1.5, -1, convert_bytes(1024 ** i, unit_only=True))

# Set the labels for the axes
axes.set_xlabel('Disk usage [bytes]', labelpad=10)
axes.set_ylabel('Process number')

# Set the limits for the axes
axes.set_xlim(0.1, 1E21)
axes.set_ylim(16, -2)

# Define the legend handles
handles=[
    Line2D([], [], label='Single-process usage', markeredgecolor="none", marker='o', markersize=3, markerfacecolor="black", linewidth=0),
    Line2D([], [], label='Cumulative usage', markeredgecolor="black", marker='o', markersize=5, markerfacecolor="none", linewidth=0),
]

# Create the legend
legend_frame = axes.legend(handles=handles, facecolor='w', framealpha=1, frameon=True, loc='lower left', edgecolor='none')

# Highlight the process categories
axes.axhspan(-0.5, 5.5, xmin=0., xmax=0.075, color=palette_ref[0])
axes.axhspan(5.5, 10.5, xmin=0., xmax=0.075, color=palette_ref[1])
axes.axhspan(10.5, 12.5, xmin=0., xmax=0.075, color=palette_ref[2])
axes.axhspan(12.5, 14.5, xmin=0., xmax=0.075, color=palette_ref[3])

# Add text for the process categories
trans = transforms.blended_transform_factory(axes.transAxes, axes.transData)
text_kwargs = dict(
    horizontalalignment='center',
    verticalalignment='center',
    color='k',
    rotation=-90,
    transform=trans,
    zorder=100    
)
axes.text(0.075 / 2, 2.5, r'Parent box', **text_kwargs, fontsize=10)
axes.text(0.075 / 2, 8, r'Zoom set-up', **text_kwargs, fontsize=10)
axes.text(0.075 / 2, 11.5, r'Calibration', **text_kwargs, fontsize=8)
axes.text(0.075 / 2, 13.5, r'Analysis', **text_kwargs, fontsize=8)

# Save the output image
plt.savefig('pipeline_data_size.pdf')
