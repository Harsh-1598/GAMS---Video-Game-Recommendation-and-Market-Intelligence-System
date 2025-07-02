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
data['Year'] = np.where(data['Year'] == 'N/A', 'Others', data['Year']) 
# data['Year'] = data['Year'].fillna('Others')
# data['Year'] =  data['Year'].replace("N/A", "Others")

# All the three lines above are doing the same work but in the different ways, like in the first and third line the string 'N/A' is converted into the string 'Others' while in the second line the missing value will be converted into the string 'Others'. In this case scenario the second line is useless.

data['Publisher'].isna()                                                 #Finding if any missing values fresent in the Publisher
data['Publisher'] = data['Publisher'].fillna('Others')                   #Automatically fills all the missing values with the string 'Others'
print(data.isnull().sum(), '\n')                                         #Checking if any missing values left in the features

#We dealt with the missing values of the year and publisher differently because in the case of the Year the 'N/A' is string value which is getting replaced by another string 'Undefined' but in the case of the Publisher the value N/A is an actual missing value so the fillna function converts all the missing values to the string 'Others' automatically. We can drop the missing values rows and columns but it might remove the other important informations.

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
plt.rcParams['font.family'] = 'Segoe UI Emoji' #Changing the font of the plot so that it supports the emojis.

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
    
print("\n", data['Publisher'].unique())
Publisher_name = input(" \n Enter the name of the Publisher:")
publisher_data(Publisher_name)

print("\n", data['Genre'].unique())
Genre_name = input(" \n Enter the Genre:")
genre_data(Genre_name)

from sklearn.preprocessing import OneHotEncoder

# One-Hot Encoding the following categorical features
encoder = OneHotEncoder(sparse_output=False)  # Make sure it's dense for DataFrame
encoded = encoder.fit_transform(data[['Genre', 'Platform', 'Year', 'Publisher']]) # One-Hot Encoding the categorical features
encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(['Genre', 'Platform', 'Year', 'Publisher'])) # Convert to DataFrame with column names
data_encoded = pd.concat([data.reset_index(drop=True), encoded_df], axis=1) # Combine with original data
# data1 = pd.get_dummies(data=data, columns=['Platform', 'Genre', 'Year', 'Publisher']) ----> The whole above four lines can also be done via this line alone.

print("\nThe change in the shape after the one-hot encoder is applied", data_encoded.shape)
print(data_encoded.info())
print(data_encoded.head())

from sklearn.metrics.pairwise import cosine_similarity

required_feature = data_encoded.drop(columns=['Genre', 'Year', 'Platform', 'Name', 'Publisher'])
print(required_feature.head())
similarity_matrix = cosine_similarity(required_feature)
print(similarity_matrix.shape)

import re
from difflib import SequenceMatcher

# Cache for normalized names and aliases (computed once)
_normalized_cache = {}
_aliases_cache = None
_platform_cache = {}

def normalize_game_name(name):
    """
    Normalize game names for better matching (with caching)
    """
    if not isinstance(name, str):
        return ""
    
    # Check cache first
    if name in _normalized_cache:
        return _normalized_cache[name]
    
    # Convert to lowercase
    normalized = name.lower().strip()
    
    # Remove special characters and extra spaces
    normalized = re.sub(r'[^\w\s]', ' ', normalized)
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    # Common replacements (optimized with single pass)
    replacements = [
        (' iii', ' 3'), (' ii', ' 2'), (' iv', ' 4'), (' v', ' 5'),
        (' vi', ' 6'), (' vii', ' 7'), (' viii', ' 8'), (' ix', ' 9'), (' x', ' 10'),
        ('grand theft auto', 'gta'), ('call of duty', 'cod'), ('battlefield', 'bf'),
        ('assassins creed', 'ac'), ('assassin s creed', 'ac'), ('mortal kombat', 'mk'),
        ('street fighter', 'sf'), ('final fantasy', 'ff'), ('red dead redemption', 'rdr'),
        ('elder scrolls', 'tes'), ('and', ''), ('the', ''), ('of', ''), ('a', ''), ('an', ''),
    ]
    
    for old, new in replacements:
        normalized = normalized.replace(old, new)
    
    # Remove extra spaces
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    # Cache result
    _normalized_cache[name] = normalized
    return normalized

def get_game_aliases():
    """
    Get cached aliases dictionary (computed once)
    """
    global _aliases_cache
    if _aliases_cache is not None:
        return _aliases_cache
    
    _aliases_cache = {
        # GTA Series
        'gta5': 'grand theft auto v', 'gtav': 'grand theft auto v',
        'gta 5': 'grand theft auto v', 'gta v': 'grand theft auto v',
        'gta4': 'grand theft auto iv', 'gtaiv': 'grand theft auto iv',
        'gta 4': 'grand theft auto iv', 'gta iv': 'grand theft auto iv',
        'gta3': 'grand theft auto iii', 'gtaiii': 'grand theft auto iii',
        'gta 3': 'grand theft auto iii', 'gta iii': 'grand theft auto iii',
        
        # Assassin's Creed
        'ac3': 'assassins creed iii', 'ac 3': 'assassins creed iii',
        'assassins creed 3': 'assassins creed iii', 'assassin s creed 3': 'assassins creed iii',
        'assassin s creed iii': 'assassins creed iii', 'ac2': 'assassins creed ii',
        'ac 2': 'assassins creed ii', 'assassins creed 2': 'assassins creed ii',
        'assassin s creed 2': 'assassins creed ii', 'assassin s creed ii': 'assassins creed ii',
        
        # Call of Duty
        'cod': 'call of duty', 'cod4': 'call of duty 4 modern warfare',
        'cod mw': 'call of duty modern warfare', 'cod mw2': 'call of duty modern warfare 2',
        'cod mw3': 'call of duty modern warfare 3', 'cod bo': 'call of duty black ops',
        'cod black ops': 'call of duty black ops',
    }
    
    return _aliases_cache

def similarity_score(a, b):
    """Optimized similarity calculation"""
    if a == b:
        return 1.0
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()

def get_platform_games(data_encoded, platform):
    """
    Get cached platform-filtered games to avoid repeated filtering
    """
    if platform in _platform_cache:
        return _platform_cache[platform]
    
    filtered_data = data_encoded[data_encoded['Platform'].str.upper() == platform.upper()]
    _platform_cache[platform] = filtered_data
    return filtered_data

def find_best_game_match(game_name, data_encoded, platform=None, threshold=0.6):
    """
    Optimized game matching with early exits and reduced iterations
    """
    game_name_lower = game_name.lower().strip()
    
    # Normalize platform once
    if platform:
        platform = platform.upper().strip()
    
    # Check aliases first (fastest check)
    aliases = get_game_aliases()
    normalized_input = normalize_game_name(game_name)
    
    if normalized_input in aliases:
        game_name_lower = aliases[normalized_input]
    
    # Determine search dataset once
    search_data = get_platform_games(data_encoded, platform) if platform else data_encoded
    
    # Try exact match first (fastest)
    exact_matches = search_data[search_data['Name'].str.lower() == game_name_lower]
    if not exact_matches.empty:
        idx = exact_matches.index[0]
        return idx, 1.0, exact_matches.iloc[0]['Name']
    
    # Fuzzy matching with optimizations
    best_match_idx = None
    best_score = threshold  # Start with threshold to avoid unnecessary comparisons
    best_name = ""
    
    # Pre-compute normalized input variations
    normalized_no_spaces = game_name_lower.replace(' ', '')
    
    # Limit search for performance (sample if dataset is very large)
    search_limit = min(1000, len(search_data))  # Process max 1000 games for fuzzy matching
    search_sample = search_data.head(search_limit) if len(search_data) > search_limit else search_data
    
    for idx, row in search_sample.iterrows():
        game_in_db = row['Name']
        if not isinstance(game_in_db, str):
            continue
        
        game_in_db_lower = game_in_db.lower()
        
        # Quick similarity checks (ordered by speed)
        # 1. Exact match (already done above)
        # 2. Contains check (very fast)
        if game_name_lower in game_in_db_lower or game_in_db_lower in game_name_lower:
            score = 0.8  # High score for substring matches
        else:
            # 3. Fuzzy matching (slower, only if needed)
            scores = [
                similarity_score(game_name_lower, game_in_db_lower),
                similarity_score(normalized_input, normalize_game_name(game_in_db)),
                similarity_score(normalized_no_spaces, game_in_db_lower.replace(' ', ''))
            ]
            score = max(scores)
        
        if score > best_score:
            best_score = score
            best_match_idx = idx
            best_name = game_in_db
            
            # Early exit for very high scores
            if score > 0.95:
                break
    
    return (best_match_idx, best_score, best_name) if best_match_idx is not None else (None, 0, "")

def recommend_games_filtered(game_name, platform=None, num_recommendations=5, filter_genre=True, filter_publisher=True, filter_decade=True, filter_platform=True):
    """
    Optimized game recommendation with reduced memory usage and faster processing
    """
    
    # Normalize platform input once
    normalized_platform = platform.upper().strip() if platform else None
    
    # Find game with optimized matching
    match_result = find_best_game_match(game_name, data_encoded, normalized_platform)
    
    if match_result[0] is None:
        print("❌ Game not found. Please check name/platform.")
        
        # Optimized suggestions (limit dataset and iterations)
        print("\n💡 Did you mean one of these games?")
        suggestions = []
        
        # Limit suggestion search for performance
        search_data = get_platform_games(data_encoded, normalized_platform) if normalized_platform else data_encoded
        search_limit = min(500, len(search_data))  # Limit suggestion search
        
        game_name_lower = game_name.lower()
        
        for idx, row in search_data.head(search_limit).iterrows():
            if isinstance(row['Name'], str):
                # Quick similarity check
                score = similarity_score(game_name_lower, row['Name'].lower())
                if score > 0.3:
                    suggestions.append((row['Name'], row['Platform'], score))
                    
                # Limit suggestions collection
                if len(suggestions) >= 20:  # Collect max 20, show top 5
                    break
        
        # Show top 5 suggestions
        suggestions.sort(key=lambda x: x[2], reverse=True)
        for i, (name, plat, score) in enumerate(suggestions[:5]):
            print(f"   {i+1}. {name} ({plat}) - similarity: {score:.2f}")
        
        return

    idx, match_score, matched_name = match_result
    
    # Show match info
    if match_score < 1.0:
        print(f"🔍 Found closest match: '{matched_name}' (similarity: {match_score:.2f})")
    
    game_row = data_encoded.loc[idx]
    
    # Extract properties once
    genre = game_row['Genre']
    publisher = game_row['Publisher']
    year = game_row['Year']
    name = game_row['Name']
    platform_val = game_row['Platform']
    
    # Calculate decade once
    decade = None
    if year != 'Others':
        try:
            decade = (int(float(year)) // 10) * 10
        except (ValueError, TypeError):
            decade = None

    # Optimized similarity calculation with early filtering
    filtered_scores = []
    seen_names = {name.lower()}  # Use set for O(1) lookups
    
    # Pre-filter data based on active filters to reduce similarity calculations
    search_candidates = data_encoded
    
    # Apply filters to reduce dataset size before similarity calculation
    if filter_platform and platform_val:
        search_candidates = search_candidates[search_candidates['Platform'] == platform_val]
    if filter_genre:
        search_candidates = search_candidates[search_candidates['Genre'] == genre]
    if filter_publisher:
        search_candidates = search_candidates[search_candidates['Publisher'] == publisher]
    if filter_decade and decade is not None:
        decade_mask = search_candidates['Year'] != 'Others'
        if decade_mask.any():
            search_candidates = search_candidates[decade_mask]
            try:
                decade_values = search_candidates['Year'].astype(float).astype(int)
                decade_matches = ((decade_values // 10) * 10) == decade
                search_candidates = search_candidates[decade_matches]
            except (ValueError, TypeError):
                pass
    
    # Remove self from candidates
    search_candidates = search_candidates[search_candidates.index != idx]
    
    # Calculate similarities only for filtered candidates
    if not search_candidates.empty:
        # Vectorized similarity calculation for better performance
        similarity_scores = []
        for i in search_candidates.index:
            score = similarity_matrix[idx, i] if hasattr(similarity_matrix, 'shape') else similarity_matrix[idx][i]
            similarity_scores.append((i, score))
        
        # Sort once and take top results
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Filter duplicates and collect results
        for i, score in similarity_scores:
            if len(filtered_scores) >= num_recommendations:
                break
                
            row = data_encoded.loc[i]
            
            # Skip duplicates (O(1) lookup)
            if row['Name'].lower() in seen_names:
                continue
            
            seen_names.add(row['Name'].lower())
            filtered_scores.append((i, score))

    # Display results (unchanged for functionality)
    print(f"\n🎮 Top {len(filtered_scores)} Recommendations for '{game_name}' [{platform or 'Any'}]:")
    
    # Show active filters
    active_filters = []
    if filter_genre:
        active_filters.append(f"Genre: {genre}")
    if filter_publisher:
        active_filters.append(f"Publisher: {publisher}")
    if filter_decade and decade:
        active_filters.append(f"Decade: {decade}s")
    if filter_platform and platform_val:
        active_filters.append(f"Platform: {platform_val}")
    
    if active_filters:
        print("🔍 Active Filters:")
        for filter_info in active_filters:
            print(f"   📌 {filter_info}")
    
    if not filtered_scores:
        print("⚠️ No recommendations found with current filters.")
        print("💡 Try disabling some filters to get more results.")
        return

    print(f"\n📋 Recommendations:")
    for rank, (i, score) in enumerate(filtered_scores, 1):
        rec = data_encoded.loc[i]
        print(f"{rank}. {rec['Name']} ({rec['Platform']}) | Genre: {rec['Genre']} | Year: {rec['Year']} | Score: {score:.2f}")

def recommend_games_filtered_safe(game_name, platform=None, num_recommendations=5, filter_genre=True, filter_publisher=True, filter_decade=True, filter_platform=True):
    """
    Optimized safe wrapper with input validation
    """
    # Convert inputs efficiently
    filters = [filter_genre, filter_publisher, filter_decade, filter_platform]
    converted_filters = []
    
    for f in filters:
        if isinstance(f, str):
            converted_filters.append(f.lower() == 'true')
        else:
            converted_filters.append(bool(f))
    
    # Convert number
    if isinstance(num_recommendations, str):
        try:
            num_recommendations = int(num_recommendations)
        except ValueError:
            print(f"⚠️ Invalid number of recommendations: {num_recommendations}. Using default value of 5.")
            num_recommendations = 5
    
    # Handle platform
    if platform == '' or platform == 'none':
        platform = None
    
    return recommend_games_filtered(game_name, platform, num_recommendations, *converted_filters)

def get_user_recommendations():
    """
    Optimized user input function
    """
    game_name = input("Enter the name of the Game: ").strip()
    platform = input("Enter the platform of the Game (or press Enter for any): ").strip()
    platform = platform.upper() if platform else None
    
    try:
        num_recommendations = int(input("Enter the no. of recommendations: "))
    except ValueError:
        print("Invalid input for recommendations. Using default value of 5.")
        num_recommendations = 5
    
    # Batch input processing
    filter_inputs = [
        input("Enter true or false to filter genre: ").strip().lower() == 'true',
        input("Enter true or false to filter publisher: ").strip().lower() == 'true',
        input("Enter true or false to filter decade: ").strip().lower() == 'true',
        input("Enter true or false to filter platform: ").strip().lower() == 'true'
    ]
    
    recommend_games_filtered(game_name, platform, num_recommendations, *filter_inputs)

# Clear caches function (optional - for memory management)
def clear_caches():
    """Clear all caches to free memory"""
    global _normalized_cache, _aliases_cache, _platform_cache
    _normalized_cache.clear()
    _aliases_cache = None
    _platform_cache.clear()

get_user_recommendations()
