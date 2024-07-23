# Title: Human phenogram for plotting variants
# Author: Dr. Alice M. Godden
# GRCh38 ncbi_refeq track used from table browser ucsc to plot exons



import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.patches import Ellipse
from matplotlib.lines import Line2D

# Define file paths
input_file = 'T0xT4_cov200.csv'  # Replace with your CSV file path
# Read the input CSV file
data = pd.read_csv(input_file)

# Check for NaN values in the 'Sample' column and handle them
if data['Sample'].isnull().any():
    print("Found NaN values in 'Sample' column. Removing rows with NaN values.")
    data = data.dropna(subset=['Sample'])

# Assign colors to samples
samples = data['Sample'].unique()
palette = sns.color_palette("Blues", len(samples))
sample_colors = {sample: color for sample, color in zip(samples, palette)}

# Read the centromere file
chrcen_data = []
with open('centromere_grch38') as f:
    for line in f:
        chrom, pos = line.split()
        chrcen_data.append((chrom, int(pos)))

# Read the genes file
genes_data = []
with open('GRCh38_genes') as f:
    for line in f:
        chrom, pos, gene = line.split()
        genes_data.append((chrom, int(pos), gene))

# Read the chromosome end file
end_data = []
with open('GRCh38_chrom_length.txt') as f:
    for line in f:
        chrom, pos = line.split()
        end_data.append((chrom, int(pos)))

# Function to map chromosomes
def get_chrom_number(chrom):
    if chrom == "chrX":
        return 23
    elif chrom == "chrY":
        return 24
    else:
        return int(chrom.replace("chr", ""))

# Create the plot
fig, ax = plt.subplots(figsize=(15, 8))

# Plot each sample with a different color
for sample in samples:
    sample_data = data[data['Sample'] == sample].copy()
    sample_data['subjChr'] = sample_data['subjChr'].apply(get_chrom_number)
    ax.scatter(sample_data['subjChr'], sample_data['subjStart'], color=sample_colors[sample], label=sample, alpha=0.5)

# Add ellipses for each half of the chromosome
for i, (chrom, end) in enumerate(end_data):
    chrom_num = get_chrom_number(chrom)
    centromere_position = next(cen for chr_name, cen in chrcen_data if chr_name == chrom)

    # Add ellipse for the first half of the chromosome (from 0 to centromere)
    ax.add_patch(
        Ellipse((chrom_num, centromere_position / 2), 0.27, centromere_position, edgecolor='black', linewidth=0.4,
                fill=False, zorder=20))

    # Add ellipse for the second half of the chromosome (from centromere to end)
    ax.add_patch(
        Ellipse((chrom_num, (end + centromere_position) / 2), 0.27, end - centromere_position, edgecolor='black',
                linewidth=0.4, fill=False, zorder=20))

# Add centromere diamonds
for chrom, cen in chrcen_data:
    chrom_num = get_chrom_number(chrom)
    ax.plot([chrom_num], [cen], marker='D', markersize=3.75, markerfacecolor="grey", color='grey', zorder=21)

# Add the genes data as text labels with marks
for chrom, pos, gene in genes_data:
    chrom_num = get_chrom_number(chrom)
    ax.annotate(gene, xy=(chrom_num, pos), ha='center', va='center', fontsize=8, fontweight='bold',
                arrowprops=dict(arrowstyle="<-", facecolor='none', linewidth=0))

# Function to read DOPEs file
def read_dopes_file(dopes_file):
    dopes_data = []
    with open(dopes_file) as f:
        next(f)  # Skip header line
        for line in f:
            fields = line.split()
            chrom = fields[1].replace("chr", "")
            chromStart = int(fields[2])
            chromEnd = int(fields[3])
            name = fields[4]
            score = int(fields[5])
            rawScore = float(fields[6])
            log2RawScore = float(fields[7])
            dopes_data.append((chrom, chromStart, chromEnd, name, score, rawScore, log2RawScore))
    return dopes_data

# Add exons data next to the ellipse
for chrom, chromStart, chromEnd in read_dopes_file('GRCh38_exon.txt'):
    chrom_num = get_chrom_number(f'chr{chrom}')
    ax.hlines(y=[chromStart, chromEnd], xmin=chrom_num, xmax=chrom_num, color='darkblue', linewidth=0.2)

# Customizing plot details
plt.xlabel('Chromosome', fontsize=18, fontweight='bold')
plt.ylabel('Position', fontsize=18, fontweight='bold')
plt.title('Human: T0 x T4, cov > 200', fontsize=20, fontweight='bold')
chrom_labels = [i for i in range(1, 25)]
ax.set_xticks(chrom_labels)
ax.set_xticklabels([f'chr{i}' for i in range(1, 23)] + ['chrX', 'chrY'], fontsize=8, fontweight='bold')
plt.yticks(fontsize=18, fontweight='bold')

# Customize legend
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=sample)
    for sample, color in sample_colors.items()
] + [
    Line2D([0], [0], color='darkblue', lw=2, label='exons'),
    Line2D([0], [0], marker='D', color='w', markerfacecolor='grey', markersize=8, label='Centromere')
]
plt.legend(handles=legend_elements, fontsize=12, loc='upper right')

# Save and display the plot
output_file = 'human_t0_t4.png'  # Replace with your desired filename and extension
plt.savefig(output_file, dpi=600)
plt.show()

