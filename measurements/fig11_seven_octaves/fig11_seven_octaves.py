# SPDX-License-Identifier: MIT
#
# Copyright (c) 2026 The authors

import pandas as pd
import matplotlib.pyplot as plt


files = [
    "14080.csv",
    "7040.csv",
    "3520.csv",
    "1760.csv",
    "880.csv",
    "440.csv",
    "220.csv",
    "110.csv",
]

labels = [
    "14080Hz",
    "7040Hz",
    "3520Hz",
    "1760Hz ",
    "880Hz ",
    "440Hz ",
    "220Hz ",
    "110Hz ",
]

freq_min = 27
freq_max = 14080*2
db_min = -42
db_max = 3

x_ticks = [55,110,220,440,880,1760,3520,7040,14080,2*14080]
y_ticks = [0,-12,-24,-36,-48]  

title = ""
output_file = "fig11_seven_octaves.png"

CALIBRATION_OFFSET = 47.8

dpi = 300
figsize = (12, 4)
linewidth = 3
colors = ['#111111', '#222222', '#333333', '#555555', '#666666', '#777777', '#999999', '#AAAAAA', '#BBBBBB']

def plot(files, labels, freq_min, freq_max, db_min, db_max, title, output_file 
         ,x_ticks=None, y_ticks=None, dpi=300, figsize=(12,5), linewidth=0.5, colors=colors):
    fig, ax = plt.subplots(figsize=figsize)
    
    for i, (file, label) in enumerate(zip(files, labels)):
        df = pd.read_csv(file, sep=';', skiprows=1, 
                        names=['Frequency', 'Power'], decimal='.')

        df['Power'] = df['Power'] + CALIBRATION_OFFSET

        color = colors[i % len(colors)]
        ax.plot(df['Frequency'], df['Power'], 
               linewidth=linewidth, color=color, label=label)        
    ax.set_xscale('log')
    ax.set_xlim(freq_min, freq_max)
    ax.set_ylim(db_min, db_max)

    if x_ticks:
        ax.set_xticks(x_ticks)
        ax.set_xticklabels([str(int(x)) if x >= 1 else str(x) for x in x_ticks])
    
    if y_ticks:
        ax.set_yticks(y_ticks)

    ax.set_xlabel('Frequency [Hz]', fontsize=19)
    ax.set_ylabel('Magnitude [dB]', fontsize=19)
    ax.set_title(title, fontsize=21, fontweight='bold')

    ax.grid(True, which='major',
        linewidth=0.3,
        color='#8A8A8A',
        alpha=1.0)

    ax.grid(True, which='minor',
        linewidth=0.1,
        color='#B0B0B0',
        alpha=1.0,
        linestyle=':')
    ax.axhline(y=-12,ls='--', color='#1A1A1A',  linewidth=2, alpha=1)
    ax.legend(fontsize=15)
    plt.tight_layout()
    for lab in ax.get_xticklabels():
        lab.set_fontsize(17)
    for lab in ax.get_yticklabels():
        lab.set_fontsize(16)

    plt.savefig(output_file, dpi=dpi, bbox_inches='tight')   
    return fig, ax

if __name__ == "__main__":
    plot(files, labels, freq_min, freq_max, db_min, db_max, 
         title, output_file, x_ticks, y_ticks, dpi, figsize, linewidth, colors)

