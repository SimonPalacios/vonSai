from functools import reduce

import pandas as pd


def remove_parentesis(row: str):
    i = row.find('(')
    return row[i + 1:-1] if i > 0 else row


def join_cols(dfs: list[pd.DataFrame], cols_name: list[str]) -> pd.DataFrame:
    for i, df in enumerate(dfs):
        df.loc[:, 2] = True
        df.columns = ['Codigo', cols_name[i]]
        df.set_index('Codigo', inplace=True)
    df = reduce(lambda fdf, ndf: fdf.join(ndf), dfs).fillna(False)
    return df


def filtrar_codigos(df: pd.DataFrame) -> pd.DataFrame:
    df2 = df[1].apply(lambda name: name[2:] if name[:2].isdigit() else name)
    df.loc[:, 1] = df2
    return df


def modelar(path):
    df = pd.read_excel(path,
                       index_col=None, header=None)
    df.drop(axis=1, columns=[0, 3], inplace=True)
    # Columnas --> Cod=1, Estado=2, Resultado=4
    # Elimino los valores nan
    df.dropna(inplace=True)
    # descarto la fila de headers del excel
    df.drop(df.index[0], inplace=True)
    # Descarto las filas de finales y cursadas desaprobadas
    excluidas = ('Reprobado', 'Abandonó', 'Desaprobado', 'Libre')
    df.drop(df[df[4].apply(lambda row: row in excluidas)].index, inplace=True)

    # Descarto la columna de resultados
    df.drop(axis=1, columns=4, inplace=True)
    # Me quedo con los códigos de las materias
    df[1] = df[1].apply(remove_parentesis)
    ingles = df[df[1].str.contains('SI208')]
    mat4 = df[df[1].str.contains('00F35')]
    if not mat4.empty:
        df.loc[mat4.loc[:, 1].index, 1] = "SI409"
    if not ingles.empty and ingles[2].values != 'Equivalencia total':
        df.loc[ingles.loc[:, 1].index, 2] = 'Cursada'

    # Ordeno primero por codigo y despues por estado (Cursada, Examen)
    df.sort_values(by=[1, 2], inplace=True)
    df = filtrar_codigos(df)
    cursadas = df[df[2].isin(['Equivalencia total', 'Cursada'])]
    finales = df[df[2].isin(['Equivalencia total', 'Examen'])]
    return join_cols([cursadas, finales], ['Cursadas', 'Finales'])

