# Author: Jeff Davids
# Modified: 
# Company: TU Delft
# Date: 171208
# Date Modified:
# Purpose: Create 3x3 array of stacked area plots for land uses and other independent variable data
# v1.3
#
# Instructions: modify file paths, colors, etc. and run
#
#   Import system modules

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# define variables

inputFilePath = r"C:\_MyDocs\OneDrive\_H2oTechDocs\Data\_Scripts\StackPlot\Input"
outputFilePath = r"C:\_MyDocs\OneDrive\_H2oTechDocs\Data\_Scripts\StackPlot\Output"

labels = ["Built Low", "Built High", "Forest", "Shrubland", "Ag Rice", "Ag non-Rice"]

colors = ["#d8b365", "#8c510a", "#2f8024", "#f6e8c3", "#01665e", "#5ab4ac"]

f, ((ax1a, ax2a, ax3a), (ax4a, ax5a, ax6a), (ax7a, ax8a, ax9a)) = plt.subplots(3, 3, dpi=300, figsize=(10, 6), sharey=False)

ax1b = ax1a.twinx
ax2b = ax2a.twinx
ax3b = ax3a.twinx
ax4b = ax4a.twinx
ax5b = ax5a.twinx
ax6b = ax6a.twinx
ax7b = ax7a.twinx
ax8b = ax8a.twinx
ax9b = ax9a.twinx


axM1 = [ax1a, ax2a, ax3a, ax4a, ax5a, ax6a, ax7a, ax8a, ax9a]
axM2= [ax1b, ax2b, ax3b, ax4b, ax5b, ax6b, ax7b, ax8b, ax9b]

fileName = ["Dhobi", "Bagmati", "Manohara", "Bishnumati", 
    "Kodkhu", "Hanumante", "Balkhu", "Nakkhu", "Godawari"]

""" RSA16 """
   
# Set common labels
f.text(0.5, 0.005, 'Watershed Area (km2)', ha='center', va='center')
f.text(0, 0.5, 'Land Use Proportion', ha='center', va='center', rotation='vertical')
f.text(1.0, 0.5, 'RSA Class (1 (near natural) to 5 (impaired))', ha='center', va='center', rotation='vertical', color="#022b6d")
# f.text(1.0, 0.5, 'EC (uS/cm)', ha='center', va='center', rotation='vertical', color="#022b6d")
# f.text(1.0, 0.5, 'DO (mg/l)', ha='center', va='center', rotation='vertical', color="#022b6d")
# f.text(1.0, 0.5, 'Flow (m3/s)', ha='center', va='center', rotation='vertical', color="#022b6d")
# f.text(1.0, 0.5, 'Flow (lps/km2)', ha='center', va='center', rotation='vertical', color="#022b6d")
    
i = 0

while i < 9:

    df = pd.read_csv(inputFilePath + '/' + fileName[i] + ".csv", index_col=['siteID'])
    axM1[i].stackplot(df.wA, df.bL, df.bH, df.nF, df.nS, df.aR, df.aNR, labels=labels, colors=colors)
    axM1[i].set_title(fileName[i] + " (" + str(i+1) + ")")
    axM1[i].set_ylim(-0.04,1.04)
    axM1[i].yaxis.set_major_locator(ticker.MultipleLocator(0.2))
    
    axM2[i] = axM1[i].twinx()
    axM2[i].tick_params(axis="y", colors="#022b6d")
# RSA
    axM2[i].invert_yaxis()
    axM2[i].yaxis.set_major_locator(ticker.MultipleLocator(1))
    axM2[i].set_ylim(5.2,0.8)
    axM2[i].plot(df.wA, df.rsa16, linestyle="--", marker="^", color="#022b6d")
    axM2[i].plot(df.wA, df.rsa17, linestyle="-", marker="o", color="#022b6d")
# # EC
    # axM2[i].invert_yaxis()
    # axM2[i].yaxis.set_major_locator(ticker.MultipleLocator(200))
    # axM2[i].set_ylim(1000,0)
    # axM2[i].plot(df.wA, df.ec16, linestyle="--", marker="^", color="#022b6d")
    # axM2[i].plot(df.wA, df.ec17, linestyle="-", marker="o", color="#022b6d")
# # DO
    # axM2[i].yaxis.set_major_locator(ticker.MultipleLocator(2))
    # axM2[i].set_ylim(-0.4,10.4)
    # axM2[i].plot(df.wA, df.do16, linestyle="--", marker="^", color="#022b6d")
    # axM2[i].plot(df.wA, df.do17, linestyle="-", marker="o", color="#022b6d")
# # FLOW17
    # axM2[i].yaxis.set_major_locator(ticker.MultipleLocator(0.2))
    # axM2[i].set_ylim(-0.04,1.04)
    # # axM2[i].plot(df.wA, df.flow16, linestyle="--", marker="^", color="#022b6d")
    # axM2[i].plot(df.wA, df.flow17, linestyle="-", marker="o", color="#022b6d")
# # FLOW1617
    # axM2[i].yaxis.set_major_locator(ticker.MultipleLocator(1))
    # axM2[i].set_ylim(-0.2,5.2)
    # axM2[i].plot(df.wA, df.flow16, linestyle="--", marker="^", color="#022b6d")
    # axM2[i].plot(df.wA, df.flow17, linestyle="-", marker="o", color="#022b6d")
# # FLOW17lps
    # axM2[i].yaxis.set_major_locator(ticker.MultipleLocator(5))
    # axM2[i].set_ylim(-1,26)
    # axM2[i].plot(df.wA, df.flow17lps, linestyle="-", marker="o", color="#022b6d")
    
    i += 1
  
# add label centered at the bottom

ax8a.legend(loc='upper center', bbox_to_anchor=(0.5, -0.3),
          fancybox=False, shadow=False, ncol=6)
          
plt.tight_layout()

plt.savefig(outputFilePath + '/' + 'RSA1617.png', bbox_inches='tight')
# plt.savefig(outputFilePath + '/' + 'FLOW1617.png', bbox_inches='tight')

f.clf()