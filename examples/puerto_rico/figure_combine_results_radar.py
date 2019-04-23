# Libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from math import pi

sns.set_style('white')

# Set data
df = pd.DataFrame({

'Build-back Time': [97.70, 100.0, 31.80, 45.16],
'Initial People without Power': [100.0, 100.0, 58.38, 60.99],
    '2052 Emissions': [93.09, 49.80, 100.0, 44.81],
'Average Emissions': [96.35, 75.34, 100.0, 72.74],
'LCOE': [98.70, 97.93, 100.0, 98.04],
})

order = [ 'Initial People without Power',  '2052 Emissions', 'Average Emissions', 'LCOE', 'Build-back Time']

custom_palette = [(0.380,0.380,0.380),(0.957,0.451,0.125),(.047, 0.149, 0.361),(0.847,0.000,0.067)]
# ------- PART 1: Create background

# number of variable
categories = list(df)#[1:]
categories = order
N = len(categories)

# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Initialise the spider plot
ax = plt.subplot(111, polar=True)

# If you want the first axis to be on top:
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)

# Draw one axe per variable + add labels labels yet
plt.xticks(angles[:-1], categories)

# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([25, 50, 75], ["25", "50", "75"], color="grey", size=7)
plt.ylim(0, 100)

# ------- PART 2: Add plots

# Plot each individual = each line of the data
# I don't do a loop, because plotting more than 3 groups makes the chart unreadable

# Ind1
values = df.loc[0,order].tolist()#.drop('group').values.flatten().tolist()
values.append(values[0])# += values[:0]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="Centralized - Natural Gas", color=custom_palette[0])
# ax.fill(angles, values, 'b', alpha=0.1)

# Ind2
values = df.loc[1,order].tolist()#.drop('group').values.flatten().tolist()
values.append(values[0])# += values[:0]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="Centralized - Hybrid", color=custom_palette[1])
# ax.fill(angles, values, 'r', alpha=0.1)

# Ind3
values = df.loc[2, order].tolist()#.drop('group').values.flatten().tolist()
values.append(values[0])# += values[:0]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="Distributed - Natural Gas", color=custom_palette[2])
# ax.fill(angles, values, 'g', alpha=0.1)

# Ind4
values = df.loc[3, order].tolist()#.drop('group').values.flatten().tolist()
values.append(values[0])# += values[:0]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="Distributed - Hybrid", color=custom_palette[3])
ax.set_rlabel_position(-50)
# ax.fill(angles, values, 'k', alpha=0.1)

# Add legend
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

savename = 'combined_results.png'
plt.savefig(savename, dpi=1000, bbox_inches="tight") #  bbox_inches="tight" is used to include the legend