import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


############################################################################################################################################
# MISC FUNCTINOS:

def ajustaListas(disciplinas_list, x_ax_list):

    global flagNovaTurma
    flagNovaTurma = 1  # liga o flag
    disciplinas_list.pop()  # retira a última disciplina da lista
    x_ax_list.pop()  # retira a última nota da lista x_ax também


# recebe uma lista de strings e trata de adicionar os \n em cada string aprimorpando a visualização das labels de anotação
def quebraListaStrings(lista_de_strings):

    lista_de_strings2 = []  # nova lista com as quebras

    # itera pela lista de strings pegando uma por uma para fazer a introdução dos \n em cada uma delas
    for string in lista_de_strings:
        string = quebraStrings(string)
        lista_de_strings2.append(string)

    return lista_de_strings2


# recebe uma string e adicona o \n a cada dois espaços encontrados
def quebraStrings(string):

    contador_spaces = 0

    # itera pela string para cada char pegando o index e o char propriamente dito
    for index, char in enumerate(string):
        if char == ' ' and contador_spaces != 1:
            contador_spaces += 1

        elif char == ' ':  # caso seja o segundo espaço, irá introduzir \n na string
            string = string[:index] + '\n' + string[index + 1:]
            contador_spaces = 0  # reseta contador

    return string

#############################################################################################################################################


#############################################################################################################################################
# PLOTS:


def scatterPlot(df, header):

    plt.clf()
    # pega as médias de da chave (disciplina, turma) retornando outro dataframe no padrão "SQL-style"
    media_df_agrupado = df.groupby(['Disciplina', 'Turma'], as_index=False).mean(numeric_only=True)

    # deleta tamanho da turma
    del media_df_agrupado['TamTurma']

    # separa os dados para comparar as notas médias entre turmas A e B da mesma disciplina
    for questao in header[2:-1]:  # montar um gráfico por questão
        disciplinas = []  # lista de disciplinas no gráfico
        x_ax = []  # eixo x do plot
        y_ax = []  # eixo y do plot
        flagNovaTurma = 1

        # faz as listas x y para plot
        for index, row in media_df_agrupado.iterrows():
            if row['Turma'] == 'A' and flagNovaTurma == 1:  # nova disciplina para comparar
                disciplinas.append(row['Disciplina'])  # adiciona essa disciplina na lista
                x_ax.append(row[questao])  # adiciona a nota da questao na lista
                flagNovaTurma = 0

            elif row['Turma'] == 'A' and flagNovaTurma == 0:  # a disciplina anterior só tinha turma A
                ajustaListas(disciplinas, x_ax)

            elif row['Turma'] == 'B' and flagNovaTurma == 0:  # disciplina já foi adicionada na lista
                y_ax.append(row[questao])  # adiciona a nota da questao na lista
                flagNovaTurma = 1

        if flagNovaTurma == 0:  # caso o último elemento da lista tiver somente turma A
            ajustaListas(disciplinas, x_ax)

        # quebra strings:
        disciplinas = quebraListaStrings(disciplinas)

        fig, ax = plt.subplots(figsize=(10, 10))

        plt.scatter(x=x_ax, y=y_ax, c='r', s=12)
        plt.grid()
        plt.xlabel('Nota média turma A')
        plt.ylabel('Nota média turma B')
        plt.title('Comparação das disciplinas em 20xx-x com duas turmas')

        # anota o que cada ponto no gráfico representa, ou seja, o nome das disciplinas
        for i, txt in enumerate(disciplinas):
            plt.text(x_ax[i], y_ax[i], txt, fontsize=8, horizontalalignment='center',
                     verticalalignment='bottom')

        plt.savefig('Scatter Plot - ' + questao + '.png', bbox_inches='tight')
        plt.clf()

    print('Scatter plots gerados. \n')


#############################################################################################################################################

def boxPlot(df, header):

    plt.clf()
    for h in header[2:-1]:
        plotFileNameT = "Box Plot - " + h + "-turmas.png"
        plotFileNameD = "Box Plot - " + h + "-disciplinas.png"
        fig, ax = plt.subplots(figsize=(15, 15))
        boxPlotT = sns.boxplot(ax=ax, x='Disciplina', y=h, data=df, width=0.5,
                               palette="colorblind", linewidth=2.5, hue='Turma')
        fig, ax = plt.subplots(figsize=(15, 15))
        boxPlotT.figure.savefig(plotFileNameT, format='png', dpi=100)
        boxPlotD = sns.boxplot(ax=ax, x='Disciplina', y=h, data=df, width=0.5,
                               palette="colorblind", linewidth=2.5)
        boxPlotD.figure.savefig(plotFileNameD, format='png', dpi=100)

    print('Box plots gerados. \n')


#############################################################################################################################################

def hBarPlot(df, header):

    plt.clf()
    ## Agrupa o resultado das questões por disciplina e turma ##
    df_disc_turma = df.groupby(['Disciplina', 'Turma'])
    mean_disc_turma = {}
    for group in df_disc_turma:
        # atribui à chave (disciplina, turma) a média de cada questão
        mean_disc_turma[group[0]] = group[1].mean()

    ## cria um dataframe para guardar as médias das questões de cada turma ##
    df_medias_turmas = pd.DataFrame(columns=header)

    i = 0
    for disc, turma in mean_disc_turma:

        val_questoes = []

        # faz uma lista com as médias das questões
        for v in mean_disc_turma[(disc, turma)]:
            val_questoes.append(v)

        # concatena com disciplina e turma
        val_questoes = [disc, turma] + val_questoes

        # nova linha para cada turma da disciplina
        df_medias_turmas.loc[i] = val_questoes
        i += 1

    # Agrupa por disciplina
    grupo_disciplina = df_medias_turmas.groupby(['Disciplina'])

    header.pop(0)  # Tira disciplina do header porque disciplina vai estar na coluna index
    header.pop(0)  # Tira turma do header

    df_medias_disciplinas = pd.DataFrame(columns=header)

    for group in grupo_disciplina:
        # Atribui a média da avaliação de todas turmas para a disciplina
        df_medias_disciplinas.loc[group[0]] = group[1].mean()

    del df_medias_disciplinas['TamTurma']  # remove o TamTurma para não ser plotado
    df_medias_disciplinas = df_medias_disciplinas.round(3)  # arredonda as médias para 3 casas decimais

    plt.figure(figsize=(8, 6))
    fig, ax = plt.subplots()
    ax.axvline(x=44, linewidth=2, color='r')  # linha vermelha no 44 (valor caso todas questões tenham a média 4)

    if __name__ == "__main__":

        df_medias_disciplinas.plot.barh(ax=ax, stacked=True, figsize=(12, 6), width=1, colormap='Paired', edgecolor='White')
        plt.savefig('Horizontal Bar Plot.png')

    print('Horizontal bar plot gerado. \n')


#############################################################################################################################################

if __name__ == "__main__":
    arquivo = input('Digite o nome do arquivo csv: ')

    option = 5
    while option:

        # adiciona o '.csv' no final da string inputada, caso já não tenha sido passado
        if not arquivo.endswith(".csv"):
            arquivo = arquivo + ".csv"

        df = pd.read_csv(arquivo, sep=';', error_bad_lines=False)

        header = list(df.columns.values)  # list with column names

        for h in header[2:-1]:
            # replaces NaN values with None
            df[h][df[h].isnull()] = None
            # replaces commas with dots for floats
            df[h] = df[h].str.replace(",", ".")
            # converts everything to float
            df[h] = df[h].astype(float)

        print("Options:\n")
        print("1. Scatter Plot")
        print("2. Box Plot")
        print("3. Horizontal Bar Plot")
        print("4. Change file name")
        print("0. Exit")

        option = int(input("Opção: "))

        if option == 1:
            scatterPlot(df, header)
        elif option == 2:
            boxPlot(df, header)
        elif option == 3:
            hBarPlot(df, header)
        elif option == 4:
            arquivo = input('\nDigite o novo nome do arquivo csv: ')
        elif option == 0:
            break
        else:
            print("Input inválido!\n")
