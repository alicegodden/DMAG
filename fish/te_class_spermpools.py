# Title: TE class plots
# Author: Dr. Alice M. Godden

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Data
te_classes = ['LINE', 'LTR', 'DNA', 'SATELLITE', 'SINE', 'RC']
non_counts = [15, 38, 521, 17, 26, 16]
fin_counts = [29, 66, 972, 28, 51, 15]
cen_counts = [28, 61, 1022, 30, 64, 21]
outer_counts = [21, 44, 568, 25, 32, 16]
# Define color palette
rocket_palette = sns.color_palette("mako", 4)

# Create plot
fig, ax = plt.subplots()

# Set the width of each bar
bar_width = 0.2

# Set the positions of the bars
r1 = np.arange(len(te_classes))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]
r4 = [x + bar_width for x in r3]

# Plot data with specified colors
bars1 = ax.bar(r1, non_counts, color=rocket_palette[0], width=bar_width, edgecolor='grey', label='Non-selected')
bars2 = ax.bar(r2, fin_counts, color=rocket_palette[1], width=bar_width, edgecolor='grey', label='Fin-clip')
bars3 = ax.bar(r3, cen_counts, color=rocket_palette[2], width=bar_width, edgecolor='grey', label='Central')
bars4 = ax.bar(r4, outer_counts, color=rocket_palette[3], width=bar_width, edgecolor='grey', label='Outer')

# Set x-axis labels with bold text and rotation for readability
ax.set_xlabel('TE Family', fontweight='bold')
ax.set_ylabel('TE Count', fontweight='bold')
ax.set_title('TE family counts from Retroseq', fontweight='bold')
ax.set_xticks([r + 1.5 * bar_width for r in range(len(te_classes))])
ax.set_xticklabels(te_classes, fontweight='bold')

# Set the ticks fontweight
plt.xticks(fontweight='bold')
plt.yticks(fontweight='bold')

# Add legend
plt.legend()

# Adjust spacing for better layout
plt.tight_layout()

# Save and show plot
plt.savefig('teclass_retroseq_danio_spermpools_aug24.png', dpi=600)
plt.show()
