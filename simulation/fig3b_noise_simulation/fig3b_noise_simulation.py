# SPDX-License-Identifier: MIT
#
# Copyright (c) 2026 The authors

import numpy as np
import matplotlib.pyplot as plt

fs = 12e6
N = 2**20
fg = 20000.0
gamma = 2 * np.pi * fg / fs
offset2 = 38 #Vertical offset for the ideal 2nd-order reference slope

f_desired = 1000
m = round(f_desired * N / fs)
f_test = m * fs / N
ampl = 0.987 


accu_z = 0.0
efm_fb = 0.0
y_out = np.zeros(N)
y_analog = np.zeros(N)

for n in range(N):  
    x_in = ampl * np.sin(2 * np.pi * f_test / fs * n)
    y_prev = 1.0 if y_out[n-1] == 1 else -1.0 if n > 0 else 0.0
    diff = x_in - y_prev
    accu_z = accu_z + diff * gamma
    if accu_z > 1.0: accu_z = 1.0
    if accu_z < -1.0: accu_z = -1.0
    s = accu_z + efm_fb
    if s >= 0:
        y_out[n] = 1
        efm_fb = s - 1.0
    else:
        y_out[n] = 0
        efm_fb = s + 1.0
    
    y_analog[n] = 1.0 if y_out[n] == 1 else -1.0


window = np.hanning(N)
Y = np.fft.rfft(y_analog * window)
freqs = np.fft.rfftfreq(N, 1/fs)

cg = np.sum(window) / N
mag = np.abs(Y) / (N * cg)

fund_bin = np.argmin(np.abs(freqs - f_test))
Y_dB = 20 * np.log10(mag / mag[fund_bin] + 1e-20)


smooth_bins = 2
kernel = np.ones(smooth_bins) / smooth_bins
mag_smooth = np.convolve(mag, kernel, mode='same')
Y_dB_smooth = 20 * np.log10(mag_smooth / mag[fund_bin] + 1e-20)

#NTF: u^2 / (gamma + u)
u_mag = 2 * np.pi * freqs / fs
z_inv = np.exp(-1j * u_mag)
ntf_theory = u_mag**2 / np.sqrt(gamma**2 + u_mag**2)
ntf_dB = 20 * np.log10(ntf_theory + 1e-20)


mid = slice(len(Y)//4, len(Y)//2)
offset = np.median(Y_dB[mid]) - np.median(ntf_dB[mid])
ntf_dB += offset


ntf_1st = 20 * np.log10(u_mag + 1e-20) + offset
ntf_2nd = 20 * np.log10(u_mag**2 + 1e-20) + offset + offset2



fig, ax = plt.subplots(figsize=(11.5, 12))
ax.semilogx(freqs[1:], ntf_1st[1:], 'g--', linewidth=4, alpha=1, color='black', label='Ideal 1st-order')
ax.semilogx(freqs[1:], ntf_2nd[1:], '-.', linewidth=4, alpha=1, color='black', label='Ideal 2nd-order')
ax.semilogx(freqs[1:], ntf_dB[1:], 'r-', linewidth=8, alpha=1, color='black', label='Proposed NTF')
ax.semilogx(freqs[1:], Y_dB_smooth[1:], linewidth=4, alpha=0.55, color='black', label='Simulated output')
ax.axvline(fg, color='black', ls='--', linewidth=4, alpha=0.3, label=f'$f_c$ = {fg:.0f} Hz')
ax.set_xlabel('Frequency [Hz]', fontsize=38)
ax.set_ylabel('')


ax.tick_params(axis='x', labelsize=28)   
ax.tick_params(axis='y', labelsize=28)

ax.legend(fontsize=24,loc='lower right')        
ax.set_xlim([500, fs/10])
plt.ylim([-190, 3]) 
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('fig3b_noise_simulation.png', dpi=150, bbox_inches='tight')
plt.show()
