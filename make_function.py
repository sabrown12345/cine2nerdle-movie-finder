#%% Import packages
import pandas as pd
import numpy as np
import sqlite3
#%%
def movie_finder(search_movie, search_movie_year):
    im_db = sqlite3.connect("im_db.db")

    sql_query = f'''
        SELECT *
        FROM title_basics 
        WHERE primaryTitle LIKE "%{search_movie}%" 
            AND primaryTitle NOT LIKE "%Beyond the Movie%" 
            AND startYear = {search_movie_year}
    '''
    movie_id = pd.read_sql_query(sql_query, im_db)['tconst']

    movie_id_str = ', '.join([f"'{value}'" for value in movie_id])
    sql_query = f'''
        SELECT *
        FROM principals
        WHERE tconst IN ({movie_id_str})
    '''
    actor_id = pd.read_sql_query(sql_query, im_db)['nconst']

    actor_id_str = ', '.join([f"'{value}'" for value in actor_id])
    sql_query = f'''
        SELECT *
        FROM principals
        WHERE nconst IN({actor_id_str}
            AND tconst NOT IN ({movie_id_str}))
    '''
    movie_ids_final = pd.read_sql_query(sql_query, im_db)['tconst']

    movie_ids_final_str = ', '.join([f"'{value}'" for value in movie_ids_final])
    sql_query = f'''
        SELECT *
        FROM title_basics
        WHERE tconst IN ({movie_ids_final_str})
    '''
    movie_matches = pd.read_sql_query(sql_query, im_db)
    result_df = pd.merge(movie_ids_final, movie_matches, on='tconst', how='inner')

    im_db.close()
    return(
        result_df[['primaryTitle', 'startYear']]\
            .value_counts()\
            .sort_values()\
            .reset_index()\
            .rename(columns={'primaryTitle': 'Title', 'startYear': 'Year', 0: 'Links'})\
            .head(10)
    )
#%%
movie_finder("Happy Feet", 2006)


#%%
# Tells you all table names
table_query = "SELECT name FROM sqlite_master WHERE type='table';"
pd.read_sql_query(table_query, im_db)

#%% Try scraping an active game
import pygetwindow as gw
import pyautogui
import pyperclip
import time

# Specify the title of the window you want to capture text from
window_title = "New Tab - Google Chrome"

# Find the window by title
window = gw.getWindowsWithTitle(window_title)

# Check if the window is found
if window:
    # Activate the window
    window[0].activate()

    # Wait for a moment to ensure the window is active
    time.sleep(1)

    # Copy the selected text (you might need to replace this with the actual method used in your application)
    pyautogui.hotkey('ctrl', 'c')

    # Retrieve the copied text from the clipboard
    clipboard_text = pyperclip.paste()

    # Print the extracted text
    print(clipboard_text)
else:
    print(f"Window with title '{window_title}' not found.")
