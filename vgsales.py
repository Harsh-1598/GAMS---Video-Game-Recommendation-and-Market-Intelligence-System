import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Reading the Dataset
data= pd.read_csv("vgsales.csv")

#Getting the information about the dataset
print(data.shape)
print(data.info())
print(data.columns.tolist())
print(data.isnull().sum(), '\n')  #Finding the null values present of the features

#Changing the year from the not available to undefined where year is not mentioned. 
data['Year'] = np.where(data['Year'] =='N/A', 'undefined', data['Year'])

#Merging the similar platforms
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


# Plotting the graph for the 'Number of Games: vs Platform vs Genre vs Publisher vs Year'
fig, axs = plt.subplots(2, 2, figsize=(20, 12))
fig.suptitle('Number of Games: vs Platform vs Genre vs Publisher vs Year', fontsize=16)

# --- Platform ---
platform_counts = data['Platform'].value_counts().head(15)
sns.barplot(x=platform_counts.index, y=platform_counts.values, palette='viridis', ax=axs[0, 0])
axs[0, 0].set_title('Number of Games by Platform')
axs[0, 0].set_ylabel('Count')
axs[0, 0].tick_params(axis='x', rotation=60)

# --- Genre ---
genre_counts = data['Genre'].value_counts().head(15)
sns.barplot(x=genre_counts.index, y=genre_counts.values, palette='mako', ax=axs[0, 1])
axs[0, 1].set_title('Number of Games by Genre')
axs[0, 1].tick_params(axis='x', rotation=60)

# --- Publisher ---
publisher_counts = data['Publisher'].value_counts().head(15)
sns.barplot(x=publisher_counts.index, y=publisher_counts.values, palette='coolwarm', ax=axs[1, 0])
axs[1, 0].set_title('Number of Games by Publisher')
axs[1, 0].tick_params(axis='x', rotation=90)

# --- Year ---
year_counts = data['Year'].value_counts().sort_index().tail(15)
sns.barplot(x=year_counts.index, y=year_counts.values, palette='rocket', ax=axs[1, 1])
axs[1, 1].set_title('Number of Games by Year')
axs[1, 1].tick_params(axis='x', rotation=60)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()


# Plotting the graph for the 'Global Sales: vs Platform vs Genre vs Publisher vs Year'
fig, axs = plt.subplots(2, 2, figsize=(20, 12))
fig.suptitle('Global Sales: vs Platform vs Genre vs Publisher vs Year', fontsize=16)

# --- Platform ---
platform_sales = data.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False).head(15)
sns.barplot(x=platform_sales.index, y=platform_sales.values, palette='viridis', ax=axs[0, 0])
axs[0, 0].set_title('Sales by Platform')
axs[0, 0].set_ylabel('Sales (millions)')
axs[0, 0].tick_params(axis='x', rotation=60)

# --- Genre ---
genre_sales = data.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False).head(15)
sns.barplot(x=genre_sales.index, y=genre_sales.values, palette='mako', ax=axs[0, 1])
axs[0, 1].set_title('Sales by Genre')
axs[0, 1].tick_params(axis='x', rotation=60)

# --- Publisher ---
publisher_sales = data.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=False).head(15)
sns.barplot(x=publisher_sales.index, y=publisher_sales.values, palette='coolwarm', ax=axs[1, 0])
axs[1, 0].set_title('Sales by Publisher')
axs[1, 0].tick_params(axis='x', rotation=90)

# --- Year ---
year_sales = data.groupby('Year')['Global_Sales'].sum().sort_index().tail(15)
sns.barplot(x=year_sales.index.astype(str), y=year_sales.values, palette='rocket', ax=axs[1, 1])
axs[1, 1].set_title('Sales by Year')
axs[1, 1].tick_params(axis='x', rotation=60)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()




