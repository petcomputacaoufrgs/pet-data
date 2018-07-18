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
    df[h] = df[h].astype(float)
    #df[h].apply(lambda(x): ((float(x)) if (type(x) == str)))


## group question results by subject and class ##
df_di_tu = df.groupby(['Disciplina', 'Turma'])
#df_di = df.groupby(['Disciplina'])
mean_di_tu = {}
#mean_di = {}
for group in df_di_tu:
    mean_di_tu[group[0]] = group[1].mean()
for group in df_di:
    mean_di[group[0]] = group[1].mean()

## creates new dataframe to hold means only ##
df_di_tu = pd.DataFrame(columns=header)
i=0
for key, value in mean_di_tu:
    valores = []
    for v in mean_di_tu[(key, value)]:
        valores.append(v)
    valores = [key, value] + valores
    df_di_tu.loc[i] = valores
    i+=1

print(df_di_tu)
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
