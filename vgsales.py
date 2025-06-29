import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Reading the Dataset
data= pd.read_csv("vgsales.csv")

#Getting the information about the dataset
print(data.shape)
print(data.info())
print(data.isnull().sum(), '\n')                                         #Finding the missing values present in the features

#Handling the missing values of the features: year and publisher. 
data['Year'] = np.where(data['Year'] =='N/A', 'Undefined', data['Year']) # = data['Year'].replace('N/A', 'Undefined') ----> this line could also be written like this
data['Publisher'].isna()                                                 #Finding if any missing values fresent in the Publisher
data['Publisher'] = data['Publisher'].fillna('Others')                   #Automatically fills all the missing values with the string 'Others'
print(data.isnull().sum(), '\n')                                         #Checking if any missing values left in the features

#We dealt with the missing values of the year and publisher differently because in the case of the Year the 'N/A' is string value which is getting replaced by another string 'Undefined' but in the case of the Publisher the value N/A is an actual missing value so the fillna function converts all the missing values to the string 'Others' automatically.

#Merging the similar platforms to understand the data properly.
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
sns.barplot(x=platform_counts.index, y=platform_counts.values, hue=platform_counts.index, palette='viridis', legend = False, ax=axs[0, 0])
axs[0, 0].set_title('Number of Games by Platform')
axs[0, 0].set_ylabel('Count')
axs[0, 0].tick_params(axis='x', rotation=60)

# --- Genre ---
genre_counts = data['Genre'].value_counts().head(15)
sns.barplot(x=genre_counts.index, y=genre_counts.values, hue=genre_counts.index, palette='mako', legend = False, ax=axs[0, 1])
axs[0, 1].set_title('Number of Games by Genre')
axs[0, 1].tick_params(axis='x', rotation=60)

# --- Publisher ---
publisher_counts = data['Publisher'].value_counts().head(15)
sns.barplot(x=publisher_counts.index, y=publisher_counts.values, hue=publisher_counts.index, palette='coolwarm', legend = False, ax=axs[1, 0])
axs[1, 0].set_title('Number of Games by Publisher')
axs[1, 0].tick_params(axis='x', rotation=90)

# --- Year ---
year_counts = data['Year'].value_counts().sort_index().tail(15)
sns.barplot(x=year_counts.index, y=year_counts.values, hue=year_counts.index, palette='rocket', legend = False, ax=axs[1, 1])
axs[1, 1].set_title('Number of Games by Year')
axs[1, 1].tick_params(axis='x', rotation=60)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()


# Plotting the graph for the 'Global Sales: vs Platform vs Genre vs Publisher vs Year'
fig, axs = plt.subplots(2, 2, figsize=(20, 12))
fig.suptitle('Global Sales: vs Platform vs Genre vs Publisher vs Year', fontsize=16)

# --- Platform ---
platform_sales = data.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False).head(15)
sns.barplot(x=platform_sales.index, y=platform_sales.values, hue=platform_sales.index, palette='viridis', legend = False, ax=axs[0, 0])
axs[0, 0].set_title('Sales by Platform')
axs[0, 0].set_ylabel('Sales (millions)')
axs[0, 0].tick_params(axis='x', rotation=60)

# --- Genre ---
genre_sales = data.groupby('Genre')['Global_Sales'].sum().sort_values(ascending=False).head(15)
sns.barplot(x=genre_sales.index, y=genre_sales.values, hue=genre_sales.index, palette='mako', legend = False, ax=axs[0, 1])
axs[0, 1].set_title('Sales by Genre')
axs[0, 1].tick_params(axis='x', rotation=60)

# --- Publisher ---
publisher_sales = data.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=False).head(15)
sns.barplot(x=publisher_sales.index, y=publisher_sales.values, hue=publisher_sales.index, palette='coolwarm', legend = False, ax=axs[1, 0])
axs[1, 0].set_title('Sales by Publisher')
axs[1, 0].tick_params(axis='x', rotation=90)

# --- Year ---
year_sales = data.groupby('Year')['Global_Sales'].sum().sort_index().tail(15)
sns.barplot(x=year_sales.index.astype(str), y=year_sales.values, hue=year_sales.index, palette='rocket', legend = False, ax=axs[1, 1])
axs[1, 1].set_title('Sales by Year')
axs[1, 1].tick_params(axis='x', rotation=60)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

#Plotting the graph for the publisher as per their released number of games and global sales as the year passes based on the user given publisher:
plt.rcParams['font.family'] = 'Segoe UI Emoji'

def publisher_data(Publisher_name):
    # Count total games
    count = data['Publisher'].value_counts().get(Publisher_name, 0)
    print(f"The total number of games published by {Publisher_name} is: {count}")

    # Filter data for the given publisher
    publisher = data[data['Publisher'] == Publisher_name]

    # Create the plot layout
    fig, ax = plt.subplots(2, 1, figsize=(18, 10))
    fig.suptitle(f'📊 Analysis of {Publisher_name}', fontsize=18, weight='bold')

    # 1️⃣ Games released per year
    publisher_nogr = publisher.groupby('Year').size().sort_index()

    sns.barplot(
        x=publisher_nogr.index.astype(str),
        y=publisher_nogr.values,
        hue=publisher_nogr.index.astype(str),
        palette='coolwarm',
        legend=False,
        ax=ax[0]
    )
    ax[0].set_title(f'🎮Games Released per Year by {Publisher_name}')
    ax[0].set_ylabel('Number of Games')
    ax[0].tick_params(axis='x', rotation=45)

    # 2️⃣ Global Sales per year
    publisher_gs = publisher.groupby('Year')['Global_Sales'].sum().sort_index()

    sns.barplot(
        x=publisher_gs.index.astype(str),
        y=publisher_gs.values,
        hue=publisher_gs.index.astype(str),
        palette='rocket',
        legend=False,
        ax=ax[1]
    )
    ax[1].set_title(f'💰Global Sales per Year for {Publisher_name}')
    ax[1].set_xlabel('Year')
    ax[1].set_ylabel('Total Global Sales (Millions)')
    ax[1].tick_params(axis='x', rotation=45)

    # Final touch
    plt.tight_layout(rect=[0.01, 0.03, 1, 0.97])
    plt.show()


#Plotting the graph for the Genre as per the released number of games and global sales as the year passes based on the user defined genre:
def genre_data(Genre_name):
    # Count total games
    count = data['Genre'].value_counts().get(Genre_name, 0)
    print(f"The total number of games published in {Genre_name} is: {count}")

    # Create the plot layout
    fig, ax = plt.subplots(2, 1, figsize=(18, 10))
    fig.suptitle(f'📊 Analysis of {Genre_name} Genre', fontsize=18, weight= 'bold')

    # Filter data for the given Genre
    Genre = data[data['Genre'] == Genre_name]

    # 1️⃣ Games released per year
    Genre_nogr = Genre.groupby('Year').size().sort_index()

    sns.barplot(
        x=Genre_nogr.index.astype(str),
        y=Genre_nogr.values,
        hue=Genre_nogr.index.astype(str),
        palette='coolwarm',
        legend=False,
        ax=ax[0]
    )
    ax[0].set_title(f'🎮Games Released per Year in {Genre_name} Genre')
    ax[0].set_ylabel('Number of Games')
    ax[0].tick_params(axis='x', rotation=45)

    # 2️⃣ Global Sales per year
    Genre_gs = Genre.groupby('Year')['Global_Sales'].sum().sort_index()

    sns.barplot(
        x=Genre_gs.index.astype(str),
        y=Genre_gs.values,
        hue=Genre_gs.index.astype(str),
        palette='rocket',
        legend=False,
        ax=ax[1]
    )
    ax[1].set_title(f'💰Global Sales per Year in {Genre_name} Genre')
    ax[1].set_xlabel('Year')
    ax[1].set_ylabel('Total Global Sales (Millions)')
    ax[1].tick_params(axis='x', rotation=45)

    # Final touch
    plt.tight_layout(rect=[0.01, 0.03, 1, 0.97])
    plt.show()
    

print(data['Publisher'].unique())
Publisher_name = input(" \n Enter the name of the Publisher:")
publisher_data(Publisher_name)

print(data['Genre'].unique())
Genre_name = input(" \n Enter the Genre:")
genre_data(Genre_name)
