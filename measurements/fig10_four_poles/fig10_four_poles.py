# SPDX-License-Identifier: MIT
#
# Copyright (c) 2026 The authors

import pandas as pd
import matplotlib.pyplot as plt

files = [
    "440_24.csv",
    "440_18.csv",
    "440_12.csv",
    "440_6.csv",
]

labels = [
    "24dB/oct",
    "18dB/oct ",
    "12dB/oct ",
    "6dB/oct ",
]

freq_min = 55
freq_max = 3520
db_min = -15
db_max = 1

x_ticks = [55, 110, 220, 440, 880, 1760, 3520]
y_ticks = [0,-3,-6,-9,-12,-15]

title = ""
output_file = "fig10_four_poles.png"
dpi = 300
figsize = (12, 4)
linewidth = 2

colors = ['#111111', '#555555', '#999999', '#BBBBBB']

def plot(files, labels, freq_min, freq_max, db_min, db_max, title, output_file 
         ,x_ticks=None, y_ticks=None, dpi=300, figsize=(12,7), linewidth=1.5, colors=colors):

    
    fig, ax = plt.subplots(figsize=figsize)
    CALIBRATION_OFFSET = 47.5


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
    ax.set_title(title, fontsize=19, fontweight='bold')


    ax.grid(True, which='major',
        linewidth=0.3,
        color='#8A8A8A',
        alpha=1.0)

    ax.grid(True, which='minor',
        linewidth=0.1,
        color='#B0B0B0',
        alpha=1.0,
        linestyle=':')

    ax.axvline(x=440, color='black', linewidth=1.8, alpha=0.7)
    ax.axhline(y=-3, color='#BBBBBB',  linewidth=1.2, alpha=0.7)
    ax.axhline(y=-6, color='#999999',  linewidth=1.2, alpha=0.7)
    ax.axhline(y=-9, color='#555555',  linewidth=1.2, alpha=0.7)
    ax.axhline(y=-12, color='#111111',  linewidth=1.2, alpha=0.7)
    ax.axhline(y=-71, color='black',  linewidth=1.2, alpha=0.7)


    y_ref = -59  # "0 dB Ref" level

    def abs_to_rel(y):
        return y - y_ref

    def rel_to_abs(y):
        return y + y_ref

    axr = ax.secondary_yaxis('right', functions=(abs_to_rel, rel_to_abs))
    rel_ticks = list(range(0, -55, -3))  
    axr.set_yticks(rel_ticks)
    ax.legend(fontsize=15)

    plt.tight_layout()
    for lab in ax.get_xticklabels():
        lab.set_fontsize(17)
    for lab in ax.get_yticklabels():
        lab.set_fontsize(17)

    for lab in axr.get_yticklabels():
        lab.set_fontsize(17)

    plt.savefig(output_file, dpi=dpi, bbox_inches='tight')
    
    return fig, ax

if __name__ == "__main__":
    plot(files, labels, freq_min, freq_max, db_min, db_max, 
         title, output_file, x_ticks, y_ticks, dpi, figsize, linewidth, colors)
