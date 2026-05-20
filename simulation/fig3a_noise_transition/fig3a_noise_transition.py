# SPDX-License-Identifier: MIT
#
# Copyright (c) 2026 The authors

import numpy as np
import matplotlib.pyplot as plt

fs = 12e6
N = 2**20

cutoffs = [27.5, 55, 110, 220, 440, 880, 1760, 3520]

freq_min = 10
freq_max = 200000
db_min = -120
db_max = -20

x_ticks = [10, 100, 1000, 10000,100000,1000000]
y_ticks = [-20, -40, -60, -80, -100]

output_file = "fig3a_noise_transition.png"

dpi = 150
figsize = (12, 12)
linewidth = 4

colors = ['#CCCCCC', '#BBBBBB', '#AAAAAA', '#999999', '#777777', '#555555', '#333333', '#222222', '#111111']



f = np.logspace(np.log10(freq_min), np.log10(freq_max), N)
u = 1 - np.exp(-1j * 2 * np.pi * f / fs)


gammas = [1e-2, 3e-3, 1e-3, 3e-4, 1e-4, 3e-5, 1e-5, 3e-6, 1e-6]


fig, ax = plt.subplots(figsize=figsize)

for i, gamma in enumerate(reversed(gammas)):
    ntf = u**2 / (gamma + (1 - gamma) * u)

    color = colors[i % len(colors)]

    ax.plot(
        f,
        20 * np.log10(np.abs(ntf)),
        linewidth=linewidth,
        color=color,
        label = {
            1e-2: r'$\gamma = 1\cdot10^{-2}$',
            3e-3: r'$\gamma = 3\cdot10^{-3}$',
            1e-3: r'$\gamma = 1\cdot10^{-3}$',
            3e-4: r'$\gamma = 3\cdot10^{-4}$',
            1e-4: r'$\gamma = 1\cdot10^{-4}$',
            3e-5: r'$\gamma = 3\cdot10^{-5}$',
            1e-5: r'$\gamma = 1\cdot10^{-5}$',
            3e-6: r'$\gamma = 3\cdot10^{-6}$',
            1e-6: r'$\gamma = 1\cdot10^{-6}$',
            }[gamma]
    )

ax.set_xscale('log')
ax.set_xlim(freq_min, freq_max)
ax.set_ylim(db_min, db_max)

if x_ticks:
    ax.set_xticks(x_ticks)
    ax.set_xticklabels([f"$10^{{{int(np.log10(x))}}}$" for x in x_ticks])

if y_ticks:
    ax.set_yticks(y_ticks)

ax.set_xlabel('Frequency [Hz]', fontsize=38)
ax.set_ylabel('Magnitude [dB]', fontsize=38)


ax.grid(
    True,
    which='major',
    linewidth=0.3,
    color='#8A8A8A',
    alpha=1.0
)

ax.grid(
    True,
    which='minor',
    linewidth=0.1,
    color='#B0B0B0',
    alpha=1.0,
    linestyle=':'
)


ax.legend(fontsize=24, loc='lower right')

for lab in ax.get_xticklabels():
    lab.set_fontsize(28)
for lab in ax.get_yticklabels():
    lab.set_fontsize(28)

plt.tight_layout()
plt.savefig(output_file, dpi=dpi, bbox_inches='tight')
plt.show()
