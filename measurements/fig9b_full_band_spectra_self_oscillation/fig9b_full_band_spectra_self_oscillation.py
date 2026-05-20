# SPDX-License-Identifier: MIT
#
# Copyright (c) 2026 The authors

import numpy as np
import matplotlib.pyplot as plt


NUM_FILES = 30 #30 spectrum analyzer segments covering 1 kHz - 6 MHz
FILE_PATH = "{i}.CSV"
# Plot range
FREQ_MIN = 1e3         
FREQ_MAX = 6e6         
MAG_MIN = -70       
MAG_MAX = 5           
OUTPUT_FILE = "fig9b_full_band_spectra_self_oscillation.png"
DPI = 300


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


peak_idx = np.argmax(mags)
mags_norm = mags - mags[peak_idx]
fig, ax = plt.subplots(figsize=(6, 5))
ax.semilogx(freqs, mags_norm, color='black', alpha=0.55, linewidth=2.4)


REF_FREQ = 200e3  
ref_mask = (freqs > 150e3) & (freqs < 250e3)
ref_level = np.median(mags_norm[ref_mask])
f_ref = np.logspace(np.log10(40e3), np.log10(FREQ_MAX), 200)
ref_20 = ref_level + 20 * np.log10(f_ref / REF_FREQ)
ax.plot(f_ref, ref_20, 'k--', linewidth=3.2, label='20 dB/dec')

ax.set_xlabel('Frequency [Hz]', fontsize=19)
ax.set_ylabel('Magnitude [dB]', fontsize=19)
ax.set_xlim([FREQ_MIN, FREQ_MAX])
ax.set_ylim([MAG_MIN, MAG_MAX])
ax.grid(True, which='both', alpha=0.3)
ax.legend(fontsize=17)

plt.tight_layout()
plt.savefig(OUTPUT_FILE, dpi=DPI)
plt.show()
