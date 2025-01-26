# %%
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

# Define the path to the CSV files
# Data is from https://population-pyramid.net/zh-cn/pp/%E4%B8%AD%E5%9B%BD
file_path = 'data/population-by-years/中国_*.csv'

# Read and concatenate all CSV files
all_files = glob.glob(file_path)
df_list = []

for file in all_files:
    df_temp = pd.read_csv(file)
    year = os.path.basename(file).split('_')[1].split('.')[0]
    df_temp['Year'] = int(year)
    df_list.append(df_temp)

df = pd.concat(df_list, ignore_index=True)

# Convert ages "100+" to 100
df['Age'] = df['Age'].apply(lambda x: 100 if x == "100+" else int(x))
df['BirthYear'] = df['Year'] - df['Age']
df['M'] = df['M'].map(lambda x: x/1e6)
df['F'] = df['F'].map(lambda x: x/1e6)

# There are 5 columns in the df, Age, M, F, Year, BirthYear
display(df)

# %%
sns.set_theme(style="whitegrid", context='notebook')

# Draw the population of M and F with x-axis of Year, grouped by BirthYear using seaborn
for gender in ['M', 'F']:
    plt.figure(figsize=(10, 6))

    cmap = 'viridis'  # Use a named colormap
    cmap = 'bone'

    norm = plt.Normalize(df['BirthYear'].min(), df['BirthYear'].max())
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    # Plot the lineplot in the lowest layer
    ax = sns.lineplot(x='Year', y=gender, data=df,
                      hue='BirthYear', palette=cmap, legend=False, zorder=1)

    # Additionally draw the Ages as scatters
    age_zero = df[df['Age'] == 0]
    plt.scatter(age_zero['Year'], age_zero[gender],
                color='red', label='Age 0', zorder=2)

    for age in [25, 35]:
        age_ = df[df['Age'] == age]
        plt.scatter(age_['Year'], age_[gender],
                    color='gray', label=f'Age {age}', zorder=2)

    # Scatter the mean population in the age range 25 to 35
    mean_pop = df[(df['Age'] >= 25) & (df['Age'] <= 35)].groupby(
        'Year')[gender].mean().reset_index()
    plt.scatter(mean_pop['Year'], mean_pop[gender],
                color='blue', label='Mean Age 25-35', zorder=3)

    plt.colorbar(sm, ax=ax, label='BirthYear')
    plt.title(f'Population of {gender} by Year')
    plt.xlabel('Year')
    plt.ylabel('Population')
    plt.legend(bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=4)
    plt.tight_layout()

    # Save the figure as a PNG file
    plt.savefig(f'population_{gender}.png')
    plt.show()

# ...existing code...

# %%
# %%
