import os.path
import traceback
from contextlib import contextmanager
from functools import reduce

from getPlan import LS, LI, ATIC, APU
import pandas as pd
import sqlite3
from sqlite3 import Error

from historiaAcademica import modelar

path = os.path.join('planes', 'database', 'tabla.db')


def create_connection():
    try:
        conn = sqlite3.connect(path)
        return conn
    except Error as e:
        print(traceback.print_exc())
    return None


@contextmanager
def db_ops():
    conn = create_connection()
    cur = conn.cursor()
    yield cur
    conn.commit()
    conn.close()


def create_table(df: pd.DataFrame, name: str):
    conn = create_connection()
    df.to_sql(name, con=conn, index=True, if_exists='replace')
    conn.commit()
    conn.close()


def table_planes():
    planes = [(LS, 'LS'), (LI, 'LI'), (ATIC, 'ATIC'), (APU, 'APU')]
    df_cods = [plan('2021').plan_estudios().index.to_series(name=f"{name}")
               for plan, name in planes]
    create_table(pd.DataFrame(df_cods).transpose(), 'planes')


def table_todas():
    create_table(unir(), 'todas')


def get_correlativas(carrera: LS | LI | ATIC | APU, nombre: str):
    query = f"select * from {nombre}"
    try:
        values = get(query)
    except Exception:
        df = carrera.plan_estudios()
        df.drop(axis=1,
                columns=['Nombre', 'Area', 'SubArea', 'Year', 'Semestre'],
                inplace=True)
        create_table(df, nombre)
        values = get(query)
    return values


def unir() -> pd.DataFrame:
    fecha = '2021'
    plan = pd.concat([LS(fecha).plan_estudios(),
                      LI(fecha).plan_estudios(),
                      ATIC(fecha).plan_estudios(),
                      APU(fecha).plan_estudios()])
    plan['cod'] = plan.index.tolist()
    plan.drop_duplicates(subset='cod', inplace=True)
    plan.drop(columns='cod', inplace=True)
    # Elimino las materias Base de Datos 1 y Sistemas Operativos que
    # tienen el mismo código pero con una "O" en vez de 0
    plan.drop(index=['SO303', 'SO410'], inplace=True)
    plan['Cursando'] = False
    plan['Cursada'] = False
    plan['Final'] = False
    return plan


def get_materias():
    query = f"select * from plan_estudio"
    try:
        values = get(query)
    except pd.errors.DatabaseError:
        print('Creando Tabla')
        create_table(unir(), 'todas')
        values = get(query)
    return values


def get(query) -> dict:
    with create_connection() as conn:
        val = pd.read_sql(query, conn)
        return val.to_dict()

