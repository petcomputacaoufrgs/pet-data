import numpy as np
import pandas as pd
import math


df = pd.read_csv('AvalDiscente_20xx-x.csv', sep=';', error_bad_lines=False)

#for item in df['Q1']:
#    print(str(type(item)) + ' ' +  str(item))

df['Q1'][df['Q1'].isnull()] = None
df['Q2'][df['Q2'].isnull()] = None
df['Q3'][df['Q3'].isnull()] = None
df['Q4'][df['Q4'].isnull()] = None
df['Q5'][df['Q5'].isnull()] = None
df['Q6'][df['Q6'].isnull()] = None
df['Q7'][df['Q7'].isnull()] = None
df['Q8'][df['Q8'].isnull()] = None
df['Q9'][df['Q9'].isnull()] = None
df['Q10'][df['Q10'].isnull()] = None
df['Q11'][df['Q11'].isnull()] = None

print(df)
