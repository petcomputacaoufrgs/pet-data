#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('AvalDiscente_20xx-x.csv', sep=';', error_bad_lines=False)

header = list(df.columns.values) #list with column names

for h in header[2:-1]:
    #replaces NaN values with None
    df[h][df[h].isnull()] = None
    #replaces commas with dots for floats
    df[h] = df[h].str.replace(",",".")
    #converts everything to float
    df[h] = df[h].astype(float)
    #df[h].apply(lambda(x): ((float(x)) if (type(x) == str)))


## group question results by subject and class ##
df_disc_tur = df.groupby(['Disciplina', 'Turma'])
mean_di_tu = {}
for group in df_disc_tur:
    #assigns to key (subjects, class) the mean value of each question
    mean_di_tu[group[0]] = group[1].mean()

## creates new dataframe to hold means only ##
df_disc_tur = pd.DataFrame(columns=header)
i=0
for key, value in mean_di_tu:
    valores = []
    #makes a list of all mean values
    for v in mean_di_tu[(key, value)]:
        valores.append(v)
    #concatenates with the key
    valores = [key, value] + valores
    #new row for each class
    df_disc_tur.loc[i] = valores
    i+=1

df_plot_box = df.copy()
del df_plot_box['TamTurma']

for h in header[2:-1]:
    plotFileNameT = h + "-turmas.jpg"
    plotFileNameD = h + "-disciplinas.jpg"
    fig, ax = plt.subplots(figsize=(20,20))
    boxPlotT = sns.boxplot(ax=ax, x='Disciplina', y=h, data=df, width=0.5,
                          palette="colorblind", linewidth=2.5, hue='Turma')
    fig, ax = plt.subplots(figsize=(20,20))
    boxPlotT.figure.savefig(plotFileNameT, format='jpeg', dpi=100)
    boxPlotD = sns.boxplot(ax=ax, x='Disciplina', y=h, data=df, width=0.5,
                          palette="colorblind", linewidth=2.5)
    boxPlotD.figure.savefig(plotFileNameD, format='jpeg', dpi=100)

if __name__ == "__main__":
    pass
