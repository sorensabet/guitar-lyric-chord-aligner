import os 
import numpy as np
import pandas as pd 

filename = '/Users/soren/Documents/Coding/guitar_song_generator/song.txt'

with open(filename, 'r') as f:
    text = f.read()
    
# Step 1. Split text into lines 
df = pd.DataFrame(text.split('\n'))
df.rename(columns={0: 'raw_text'}, inplace=True)
df['line'] = df.index 

# Split lines into individual words
df2 = pd.DataFrame(df['raw_text'].str.split().explode())
df2['line'] = df2.index
df2.rename(columns={'raw_text': 'raw_word'}, inplace=True)
df2['clean_word'] = df2['raw_word'].str.replace('{[A-Z]}', '')
df2['cwl'] = df2['clean_word'].str.len()
df2['cwl'] = np.where(df2['cwl'].isnull(), 0, df2['cwl'])

df2['chord'] = df2['raw_word'].str.extract(r'{([A-Z])}')
df2['cwl'] = np.where(~df2['chord'].isnull(), df2['cwl'] - 1, df2['cwl'])
df2['chord_spaces'] = df2['cwl'].apply(lambda x: ' ' * int(x))
df2['chord'] = np.where(df2['chord'].isnull(), df2['chord_spaces'], df2['chord'] + df2['chord_spaces'])

# Replace empty lines 
df2['clean_word'] = np.where(df2['clean_word'].isnull(), '\n', df2['clean_word'])
df2['chord'] = np.where(df2['chord'].isnull(), '', df2['chord'])

# Get just the columns that we need 
df3 = df2[['line', 'clean_word', 'chord']]

chord_lines = []
word_lines = []

for l in df3['line'].unique():
    tdf = df3.loc[df3['line'] == l]
    t_chord_line = ' '.join(tdf['chord']) 
    t_word_line = ' '.join(tdf['clean_word'])
    
    print(t_chord_line)
    print(t_word_line)
