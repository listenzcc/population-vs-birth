"""
File: main.py
Author: Chuncheng Zhang
Date: 2023-06-06
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Amazing things

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""


# %% ---- 2023-06-06 ------------------------
# Requirements and constants
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

from pathlib import Path

population_path = Path('population.csv')
birth_path = Path('birth.txt')

# %% ---- 2023-06-06 ------------------------
# Function and class


def read_population():
    population = pd.read_csv(population_path, sep='\t')

    population['Population'] = population['Population'].map(
        lambda e: int(e.replace(',', '')))

    population['Year'] = population['Year'].map(int)

    return population


def read_birth():
    content = [e for e in open(birth_path).readlines() if e.strip()]
    content = [e.split('年：') for e in content]

    df = pd.DataFrame(content, columns=['Year', 'Birth'])
    df['Birth'] = df['Birth'].map(lambda e: int(float(e.split('万')[0]) * 1e4))
    df['Year'] = df['Year'].map(int)

    return df


# %% ---- 2023-06-06 ------------------------
# Play ground
population = read_population()
population

# %%
birth = read_birth()
birth

# %%
data = pd.merge(birth, population, on='Year', how='outer')
data

# %% ---- 2023-06-06 ------------------------
# Pending

# %% ---- 2023-06-06 ------------------------
# Pending
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# --------------------------------------------------------------------
# Ax 0, 0
ax = axs[0, 0]
ax.plot(data['Population'], data['Birth'], c='#333a')
mappable = ax.scatter(x=data['Population'], y=data['Birth'], c=data['Year'])
ax.set_title('Birth vs population')
ax.set_ylabel('Birth')
ax.set_xlabel('Population')
ax.grid(True)
ax.set_axisbelow(True)

# --------------------------------------------------------------------
# Ax 0, 1
ax = axs[0, 1]
ax.scatter(x=data['Year'], y=data['Birth'] /
           data['Population'], c=data['Year'])

for year, halign in zip([2022, 1979], ['right', 'left']):
    color = mappable.get_cmap()(mappable.norm(year))
    query = data.query('Year=={}'.format(year)).iloc[0]
    y = query['Birth'] / query['Population']
    ax.axhline(y=y, color=color)
    ax.text(
        x=year, y=y, s='{}: {:.4f} '.format(year, y),
        horizontalalignment=halign,
        verticalalignment='bottom'
    ).set_bbox(dict(facecolor=color, alpha=0.5))

ax.set_title('Ratio (birth / population) across years')
ax.set_ylabel('Ratio')
ax.set_xlabel('Year')
ax.grid(True)
ax.set_axisbelow(True)
plt.colorbar(mappable, ax=ax)

# --------------------------------------------------------------------
# Ax (1, 0) & (1, 1)
gs = axs[1, 0].get_gridspec()
for ax in axs[1, :]:
    ax.remove()
ax = fig.add_subplot(gs[-1, 0:])

ax2 = ax.twinx()
ax2.scatter(x=data['Year'], y=data['Population'], c='#aaa5')
ax2.set_ylabel('Population')

mappable = ax.scatter(x=data['Year'], y=data['Birth'], c=data['Year'])

for year in [2022, 1979, 1942]:
    color = mappable.get_cmap()(mappable.norm(year))
    y = data.query('Year=={}'.format(year)).iloc[0]['Birth']
    ax.axhline(y=y, color=color)
    ax.text(
        x=year, y=y - 1e6, s='{}: {:.2f} Million'.format(year, y / 1e6),
        horizontalalignment='center',
        verticalalignment='top'
    ).set_bbox(dict(facecolor=color, alpha=0.5))

ax.set_title('Birth across years')
ax.set_ylabel('Birth')
ax.set_xlabel('Year')
ax.grid(True)
ax.set_axisbelow(True)

plt.tight_layout()
plt.show()


# %%
def _base(se, offset=25):
    year = se['Year']
    query = data.query('Year == {}'.format(year - offset))
    if len(query) > 0:
        return query.iloc[0]['Birth']

data['Base25'] = data.apply(_base, axis=1)
data['Base30'] = data.apply(_base, axis=1, args=(30,))
data['BirthOf25Years'] = data['Birth'] / data['Base25']
data['BirthOf30Years'] = data['Birth'] / data['Base30']
data

# %%
# ---------------------------------------------------------------
fig, ax = plt.subplots(1, 1, figsize=(8, 4))

mappable = ax.scatter(x=data['Year'], y=data['BirthOf25Years'], c=data['Year'])

for year in [2022, 1979]:
    color = mappable.get_cmap()(mappable.norm(year))
    y = data.query('Year=={}'.format(year)).iloc[0]['BirthOf25Years']
    ax.axhline(y=y, color=color)
    ax.text(
        x=year, y=y, s='{}: {:.2f}'.format(year, y),
        horizontalalignment='center',
        verticalalignment='top'
    ).set_bbox(dict(facecolor=color, alpha=0.5))

ax.set_xlabel('Year')
ax.set_ylabel('Birth per 25 years old')
ax.set_title('How many birth when they are 25 years old')
ax.grid(True)
ax.set_axisbelow(True)

plt.colorbar(mappable, ax=ax)

fig.tight_layout()


# ---------------------------------------------------------------
fig, ax = plt.subplots(1, 1, figsize=(8, 4))

mappable = ax.scatter(x=data['Year'], y=data['BirthOf30Years'], c=data['Year'])

for year in [2022, 1979]:
    color = mappable.get_cmap()(mappable.norm(year))
    y = data.query('Year=={}'.format(year)).iloc[0]['BirthOf30Years']
    ax.axhline(y=y, color=color)
    ax.text(
        x=year, y=y, s='{}: {:.2f}'.format(year, y),
        horizontalalignment='center',
        verticalalignment='top'
    ).set_bbox(dict(facecolor=color, alpha=0.5))

ax.set_xlabel('Year')
ax.set_ylabel('Birth per 30 years old')
ax.set_title('How many birth when they are 30 years old')
ax.grid(True)
ax.set_axisbelow(True)

plt.colorbar(mappable, ax=ax)

fig.tight_layout()
plt.show()

# %%
