# SPDX-License-Identifier: MIT
#
# Copyright (c) 2026 The authors

import pandas as pd
import matplotlib.pyplot as plt

files = [
    "G4.csv",
    "G3.75.csv",
    "G3.5.csv",
    "G3.csv",
    "G2.csv",
    "G1.csv",
    "G0.csv",
]

labels = [
    "g = 4",
    "g = 3.75",
    "g = 3.5",
    "g = 3",
    "g = 2 ",
    "g = 1",
    "g = 0 ",
]

freq_min = 110
freq_max = 1760
db_min = -53
db_max = 3
offset = 17.2 #calibration offset

x_ticks = [110, 220, 440,880, 1760]  
y_ticks = [0,-10,-20,-30,-40,-50]

title = ""
output_file = "fig12_resonance.png"

dpi = 300
figsize = (12, 5)
linewidth = 2.5
colors = ['#111111', '#444444', '#777777', '#AAAAAA','#BFBFBF', '#CCCCCC', '#CCCCCC']


def plot(files, labels, freq_min, freq_max, db_min, db_max, title, output_file 
         ,x_ticks=None, y_ticks=None, dpi=300, figsize=(12,7), linewidth=1.5, colors=colors):
    
    fig, ax = plt.subplots(figsize=figsize)    
    for i, (file, label) in enumerate(zip(files, labels)):
        df = pd.read_csv(file, sep=';', skiprows=1, 
                        names=['Frequency', 'Power'], decimal='.')

        df['Power'] = df['Power'] + offset
        
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
        linewidth=0.4,
        color='#8A8A8A',
        alpha=1.0)

    ax.grid(True, which='minor',
        linewidth=0.1,
        color='#B0B0B0',
        alpha=1.0,
        linestyle=':')

    ax.legend(fontsize=15)
    
    plt.tight_layout()
    for lab in ax.get_xticklabels():
        lab.set_fontsize(17)
    for lab in ax.get_yticklabels():
        lab.set_fontsize(17)
    plt.savefig(output_file, dpi=dpi, bbox_inches='tight')  
    return fig, ax

if __name__ == "__main__":
    plot(files, labels, freq_min, freq_max, db_min, db_max, 
         title, output_file, x_ticks, y_ticks, dpi, figsize, linewidth, colors)
