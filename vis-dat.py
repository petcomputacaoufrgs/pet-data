#import numpy as np
import pandas as pd

df = pd.read_csv('AvalDiscente_20xx-x.csv', sep=';', error_bad_lines=False)

header = list(df.columns.values) #list with column names

agl = []

for h in header[2:-1]:
    #replaces NaN values with None
    df[h][df[h].isnull()] = None
    #replaces commas with dots for floats
    df[h] = df[h].str.replace(",",".")
    #converts everything to float
    df[h].apply(lambda x: type(x)==str and float(x))


#group question results by subject and class
df_di_tu = df.groupby(['Disciplina', 'Turma'])
df_di = df.groupby(['Disciplina'])

#mean_di_tu = df.groupby(['Disciplina','Turma','TamTurma'])
#mean_di = []





turmas = df.groupby(['Turma'])
for group in turmas:
    print(len(group))
    #novo = pd.concat([group[1]['Disciplina'].groupby(['Disciplina']), group[1]['Turma'].groupby(['Turma'])], axis=0)
    #print(novo)
    print(group[1]['Q2'].mean())
    novo = pd.concat([group[1]['Q1'], group[1]['Q2']], axis=1)
    print(novo)
    novo = pd.concat([novo, group[1]['Q2'].mean], axis=1)
    print(novo)




"""
for h in header[2:-1]:
    #mean_di_tu[h] = pd.concat(df['Disciplina', 'Turma'].groupby(['Turma']))
    for group in turmas:
        temp = pd.concat([temp, group[1]], axis=0)
    print(temp)
"""
"""
mean_di_tu = {}
for h in header[2:-1]:
    for group in df_di_tu:
        #print(group[1]['Disciplina'])
        #print(group[1][h])
        mean_di_tu[h] = pd.concat([group[1]['Disciplina'], group[1][h]], axis=1)
    print(mean_di_tu)
"""


if __name__ == "__main__":
    print(df)
