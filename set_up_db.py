#%% Import packages
import pandas as pd
import numpy as np
import sqlite3
#%% Make database 
im_db = sqlite3.connect("im_db.db")

name_basics = pd.read_csv('name_basics.tsv', sep = '\t')
name_basics = name_basics.dropna(subset = ['primaryProfession', 'nconst', 'primaryName'])
desired_professions = ['actor', 'actress', 'director', 'composer', 
                       #'producer', 'writer'
                       ] # Type of people to keep
name_basics = name_basics[name_basics['primaryProfession'].str.contains('|'.join(desired_professions), case=False)]
name_basics = name_basics.drop(["birthYear", "deathYear", "primaryProfession", "knownForTitles"], axis = 1)
name_basics = name_basics.drop_duplicates()
name_basics.to_sql('name_basics', im_db, index = False, chunksize = 1000, if_exists = 'replace')
del name_basics
del desired_professions

title_basics = pd.read_csv('title_basics.tsv', sep = '\t')
title_basics = title_basics[title_basics['titleType'].isin(['movie'])]
title_basics = title_basics.drop(['titleType', 'endYear', 'runtimeMinutes', 'genres', 'isAdult'], axis = 1)
title_basics = title_basics.drop_duplicates()
title_basics.to_sql('title_basics', im_db, index = False, chunksize = 1000, if_exists = 'replace')
unique_tconst_values = title_basics['tconst'].unique()
del title_basics
del unique_tconst_values

principals = pd.read_csv('title_principals.tsv', sep = '\t')
desired_categories = ['director', 'composer', 'producer', 'actor', 'actress', 'writer']
principals = principals[principals['tconst'].isin(unique_tconst_values)]
principals = principals[principals['category'].isin(desired_categories)]
principals = principals.dropna(subset = ['tconst'])
principals = principals.drop(['job', 'characters', 'category', 'ordering'], axis = 1)
principals = principals.drop_duplicates()
principals.to_sql('principals', im_db, index = False, chunksize = 1000, if_exists = 'replace')
del principals

# Commit changes and close
im_db.commit()
im_db.close()

