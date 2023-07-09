import numpy as np
import pandas as pd 

def convert_lyrics(text):
    """
        Ingests the text with note positions indicated by curly brackets.
        Generates the output text
    """
    
    # Step 1. Split text into lines 
    df = pd.DataFrame(text.split('\n'))
    df.rename(columns={0: 'raw_text'}, inplace=True)
    df['line'] = df.index 


    # Split lines into individual words
    df2 = pd.DataFrame(df['raw_text'].str.split().explode())
    #df2['raw_text'] = np.where(df2['raw_text'].isnull(), '\n', df2['raw_text'])
    df2['line'] = df2.index
    df2.rename(columns={'raw_text': 'raw_word'}, inplace=True)
    df2['clean_word'] = df2['raw_word'].str.replace('\{[A-Za-z#0-9]{1,}\}', '', regex=True)
    df2['cwl'] = df2['clean_word'].str.len()
    df2['cwl'] = np.where(df2['cwl'].isnull(), 0, df2['cwl'])

    df2['chord'] = df2['raw_word'].str.extract(r'\{([A-Za-z#0-9]{1,})\}')
    df2['chord_length'] = df2['chord'].str.len()
    df2['cwl'] = np.where(~df2['chord'].isnull(), df2['cwl'] - df2['chord_length'], df2['cwl'])
    df2['chord_spaces'] = df2['cwl'].apply(lambda x: ' ' * int(x))
    df2['chord'] = np.where(df2['chord'].isnull(), df2['chord_spaces'], df2['chord'] + df2['chord_spaces'])

    # # Replace empty lines 
    df2['clean_word'] = np.where(df2['clean_word'].isnull(), '\n', df2['clean_word'])
    df2['chord'] = np.where(df2['chord'].isnull(), '', df2['chord'])

    # # Get just the columns that we need 
    df3 = df2[['line', 'clean_word', 'chord']]
    
    # Get just chords to prepare images 
    df4 = df3[['chord']]
    df4['chord'] = df4['chord'].str.replace(' |\n','',regex=True)
    df4 = df4.loc[df4['chord'] != '']
    df4.drop_duplicates(subset=['chord'], inplace=True)
    df4['path'] = '/static/images/' + df4['chord'] + '.png'
    df4['path'] = df4['path'].str.replace('#', '%23')


    final_answer_elements = []

    for l in df3['line'].unique():
        tdf = df3.loc[df3['line'] == l]
        t_chord_line = '\n' + ' '.join(tdf['chord']) + '\n'
        t_word_line = ' '.join(tdf['clean_word']) + '\n'
        
        final_answer_elements.append(t_chord_line)
        final_answer_elements.append(t_word_line)
    
    print(''.join(final_answer_elements))
    return ''.join(final_answer_elements), df4['path'].tolist()