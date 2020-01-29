import pandas as pd
import numpy as np
import sys, os, time, io
import re

source_path_file = r'./test.txt'

# load data
print( 'loading data from %s' % source_path_file )
with open( source_path_file, 'r') as f:
    s = f.read()
    raw_text = eval(s)

col_tags = ['title', 'time','author', 'main_content', 'positive_push','negative_push','neutral_push'] 
df = pd.DataFrame( columns=col_tags )

# analyzing data and reformating
print( 'analyzing data and reformating...' )
for idx, raw_data in enumerate(raw_text):
    # url = raw_data['url']
    title = raw_data['title']
    time = raw_data['time']
    author = raw_data['author']
    main_content = raw_data['main_content'].replace('\n', '\t').replace(',', '，')
    positive_push = ''.join(raw_data['positive_push']).replace('\n', '\t').replace(',', '，')
    negative_push = ''.join(raw_data['negative_push']).replace('\n', '\t').replace(',', '，')
    neutral_push = ''.join(raw_data['neutral_push']).replace('\n', '\t').replace(',', '，')
    df = df.append( pd.Series( [ title, time,author, main_content, positive_push,negative_push,neutral_push], index=col_tags), ignore_index=True )
    print( 'processing... %d/%d' %((idx+1)//len(raw_text) , len(raw_text)) )
df.replace( ['\r\n', '\n', ',', '\u3000'], [' ', ' ', '，', ' '], inplace=True, regex=False)

#generate data set
print( 'saving data...' )
df.to_csv( 'pttData.csv' ,sep=',', na_rep='', encoding='utf-8', mode='w', header=True, index=False )
print( '\tsize of dataframe: ', df.shape )
print( '\tcol tags of dataframe is: ', col_tags )

