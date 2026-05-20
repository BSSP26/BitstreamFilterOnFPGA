# SPDX-License-Identifier: MIT
#
# Copyright (c) 2026 The authors

import numpy as np
import matplotlib.pyplot as plt


NUM_FILES = 15         #15 spectrum analyzer segments covering 1 kHz - 6 MHz
FILE_PATH = "{i}.CSV"
# Plot range
FREQ_MIN = 1e3         
FREQ_MAX = 6e6         
MAG_MIN = -55         
MAG_MAX = 5          
OUTPUT_FILE = "fig9a_full_band_spectra_lfsr.png"
DPI = 300

# Passband normalization range (used to set 0 dB reference)
PB_LOW = 5e3           
PB_HIGH = 15e3

# 20 dB/dec reference line
REF_FREQ = 400e3       
REF_RANGE_LOW = 300e3  
REF_RANGE_HIGH = 500e3
REF_START = 100e3      
REF_STOP = 6e6         


all_freqs = []
all_mags = []

for i in range(NUM_FILES):
    fname = FILE_PATH.format(i=i)
    with open(fname, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            try:
                freq = float(parts[0])
                mag = float(parts[1])
                all_freqs.append(freq)
                all_mags.append(mag)
            except (ValueError, IndexError):
                continue

freqs = np.array(all_freqs)
mags = np.array(all_mags)


sort_idx = np.argsort(freqs)
freqs = freqs[sort_idx]
mags = mags[sort_idx]


_, unique_idx = np.unique(freqs, return_index=True)
freqs = freqs[unique_idx]
mags = mags[unique_idx]


mask = freqs > 100
freqs = freqs[mask]
mags = mags[mask]


pb_mask = (freqs > PB_LOW) & (freqs < PB_HIGH)
pb_level = np.max(mags[pb_mask])
mags_norm = mags - pb_level

fig, ax = plt.subplots(figsize=(6, 5))
ax.semilogx(freqs, mags_norm, color='black', alpha=0.55, linewidth=2.2)
ax.annotate('$f_c$ = 20 kHz\n−12 dB',
            xy=(20e3, -12), xytext=(60e3, -12),
            fontsize=17,
            arrowprops=dict(arrowstyle='->', color='black'),
            )


f_ref = np.logspace(np.log10(REF_START), np.log10(REF_STOP), 200)
anchor_mask = (freqs > REF_RANGE_LOW) & (freqs < REF_RANGE_HIGH)
anchor_level = np.median(mags_norm[anchor_mask])
ref_20 = anchor_level + 20 * np.log10(f_ref / REF_FREQ)
ax.plot(f_ref, ref_20, 'k--', linewidth=3.2, label='20 dB/dec')

ax.set_xlabel('Frequency [Hz]', fontsize=19)
ax.set_ylabel('Magnitude [dB]', fontsize=19)
ax.set_xlim([FREQ_MIN, FREQ_MAX])
ax.set_ylim([MAG_MIN, MAG_MAX])
ax.grid(True, which='both', alpha=0.3)
ax.legend(fontsize=17)

ax.tick_params(axis='both', which='major', labelsize=16)

plt.tight_layout()
plt.savefig(OUTPUT_FILE, dpi=DPI)
plt.show()

