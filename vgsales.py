import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data= pd.read_csv("vgsales.csv")
print(data.shape)
print(data.info())
print(data.columns.tolist())
print(data.isnull().sum(), '\n')

data['Year'] = np.where(data['Year'] =='N/A', 'undefined', data['Year'])
print(data.isnull().sum(), '\n')

print(data.value_counts('Genre', ascending=False))
Genre_data= data.value_counts('Genre', ascending=False).head(50)
plt.figure(figsize=(12, 6))
sns.barplot(x=Genre_data.index, y=Genre_data.values, palette="viridis")
plt.title("Top Genre's by Number of Games")
plt.xlabel("Genre's")
plt.ylabel("Number of Games")
plt.xticks(rotation=90)
plt.tight_layout()

print(data.value_counts('Publisher', ascending=False))
publisher_data= data.value_counts('Publisher', ascending=False).head(50)
plt.figure(figsize=(12, 6))
sns.barplot(x=publisher_data.index, y=publisher_data.values, palette="viridis")
plt.title("Top 50 Publishers by Number of Games")
plt.xlabel("Publishers")
plt.ylabel("Number of Games")
plt.xticks(rotation=90)
plt.tight_layout()

print(data.value_counts('Year', ascending=False))
Year_data= data.value_counts('Year', ascending=False).head(50)
plt.figure(figsize=(12, 6))
sns.barplot(x=Year_data.index, y=Year_data.values, palette="viridis")
plt.title("Top Years by Number of Games")
plt.xlabel("Years")
plt.ylabel("Number of Games")
plt.xticks(rotation=90)
plt.tight_layout()

PS = ['PS', 'PS2', 'PS3', 'PS4', 'PS5', 'PSV', 'PSP']
data['Platform'] = np.where(data['Platform'].isin(PS) , 'PS', data['Platform'])

XBOX = ['X360', 'XOne', 'XBOX', 'XS', 'XB']
data['Platform'] = np.where(data['Platform'].isin(XBOX) , 'XBOX', data['Platform'])

Nintendo = ['Wii', 'WiiU', 'DS', '3DS', 'Switch', 'GBA', 'GC', 'N64', 'SNES', 'NES', 'GB', 'GBC']
data['Platform'] = np.where(data['Platform'].isin(Nintendo) , 'Nintendo', data['Platform'])

Sega = ['GEN', 'SCD', 'SAT', 'DC', 'GG']
data['Platform'] = np.where(data['Platform'].isin(Sega) , 'Sega', data['Platform'])

Atari = ['2600', '5200', '7800', 'Lynx', 'Jaguar']
data['Platform'] = np.where(data['Platform'].isin(Atari) , 'Atari', data['Platform'])

Others = ['NeoGeo', 'TG16', '3DO', 'WS', 'VB', 'PCFX', 'NG']
data['Platform'] = np.where(data['Platform'].isin(Others) , 'Others', data['Platform'])

print(data.value_counts('Platform', ascending=False))
Platform_data= data.value_counts('Platform', ascending=False).head(50)
plt.figure(figsize=(12, 6))
sns.barplot(x=Platform_data.index, y=Platform_data.values, palette="viridis")
plt.title("Top Platforms by Number of Games")
plt.xlabel("Platforms")
plt.ylabel("Number of Games")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()



