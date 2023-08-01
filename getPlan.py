import os.path
import traceback
from abc import abstractmethod, ABC
from typing import List
import pandas as pd


class Plan(ABC):
    _link: str

    def __init__(self, link):
        self._link = link

    @abstractmethod
    def plan(self):
        pass

    @abstractmethod
    def optativas(self):
        pass

    @staticmethod
    def get_cods(name: str):
        cod = ""
        excepciones = ["de", "la", "al", "a", "e"]
        for word in name.split():
            cod += word[0].capitalize() \
                if word[0].isalpha() & (word[0] not in excepciones) \
                else ""
        return f"OPT-{cod if len(cod) < 4 else cod[:4]}"

    @staticmethod
    def reindexar(plan: pd.DataFrame, columnas: List[str]) -> pd.DataFrame:
        return plan.reindex(columns=columnas)

    @staticmethod
    def semester_optativas(plan):
        plan.Semestre.str.replace('°', '')

    @staticmethod
    def get_index_of_string(plan, word: str) -> List[int]:
        return plan[plan.Código.str.contains(word)].index.tolist()

    @staticmethod
    def add_columns(plan, args):
        for column, value in args:
            plan[column] = value

    @staticmethod
    def asign_value(plan, column, row, value):
        plan[column][row] = value

    def get_indexs(self, plan, words: List[str]):
        return [self.get_index_of_string(plan, word) for word in words]

    @staticmethod
    def remove_parentesis(row: str):
        i = row.find('(')
        return row[:i - 1] if i > 0 else row

    @staticmethod
    def propagar_value(plan, indices, columna, func):
        for i in range(len(indices) - 1):
            plan.loc[indices[i]:indices[i + 1], columna] = func(i)

    def year_semester(self, plan) -> None:
        indices = self.get_indexs(plan, ['SEMESTRE', 'AÑO', 'TERCER AÑO', 'SI302', 'SI307'])
        sem, year, tercero, ing2, oo2 = indices
        sem += [len(plan)]
        year = [0] + year + [len(plan)]
        tercero = tercero[0]
        self.add_columns(plan, [('Area', '-'), ('SubArea', '-')])
        plan['Area'][:tercero + 1] = 'General'
        plan['Area'][ing2] = 'General'
        plan['Area'][oo2] = 'General'
        self.propagar_value(plan, year, 'Año', lambda x: x + 1)
        self.propagar_value(plan, sem, 'Semestre', lambda x: 2 if ((x + 1) % 2 == 0) else 1)
        self.propagar_value(plan, [0, 3], 'Semestre', lambda x: 'CI')
        plan.drop(axis=0, labels=sem[:-1] + year[1:-1], inplace=True)
        plan.reset_index(inplace=True, drop=True)

    def edit_plan_optativas(self, plan):

        plan.drop(axis=1, columns=['PRESENTACIÓN', "Unnamed: 4"], inplace=True)
        plan.drop(plan.tail(1).index, inplace=True)
        plan.columns = ["Nombre", "Semestre", "Correlativas"]
        values = [('Año', '-'), ('Area', 'Optativa'), ('SubArea', '-')]
        self.add_columns(plan, values)
        columns = ["Nombre", "Correlativas", "Area", "SubArea", "Año", "Semestre"]
        plan = self.reindexar(plan, columns)
        row = self.get_index_of_string(plan, 'adicionales')
        plan["Semestre"] = plan["Semestre"].str.replace('º', '')
        plan.drop(axis=0, labels=row, inplace=True)
        plan.reset_index(inplace=True, drop=True)

    def edit_plan_regular(self, plan):
        plan.drop(axis=1, columns=["Contacto", "Duración"], inplace=True)
        plan.fillna(value='-', inplace=True)
        self.year_semester(plan)

    def _save_plan(self) -> pd.DataFrame:
        plan = pd.read_html(f"https://www.info.unlp.edu.ar/{self._link}", header=1)[0][:]
        plan.to_csv(os.path.join("planes", "pelados", f"{self._link}.csv"), index=False)
        return plan

    def _get_plan(self) -> pd.DataFrame:
        try:
            tabla = pd.read_csv(os.path.join("planes", "pelados", f"{self._link}.csv"))
            try:
                self.edit_plan_regular(tabla)
            except KeyError as ex:
                self.edit_plan_optativas(tabla)

            tabla['Nombre'] = tabla['Nombre'].apply(self.remove_parentesis)
            return tabla
        except FileNotFoundError:
            return self._save_plan()
        except Exception as ex:
            print(traceback.print_exc())

    def plan_estudios(self):
        plan = pd.concat([self.plan(), self.optativas()])
        plan.reset_index(inplace=True, drop=True)
        plan.rename(columns={'Código': 'Codigo', 'Año': 'Year'}, inplace=True)
        plan.set_index(plan['Codigo'], inplace=True)
        plan.drop(axis=1, columns='Codigo', inplace=True)
        return plan


class LS(Plan):

    def __init__(self, fecha):
        super().__init__(f"licenciatura-en-sistemas-plan-{fecha}")

    def plan(self) -> pd.DataFrame:
        plan = self._get_plan()
        tesis, opt = self.get_indexs(plan, ['0I503', '-'])
        plan.loc[tesis[0], 'Correlativas'] = '-'
        plan.loc[opt[0], 'Código'] = 'OP1LS'
        plan.loc[opt[1], 'Código'] = 'OP2LS'
        return plan

    def optativas(self) -> pd.DataFrame:
        # return self._get_plan("optativas-2023-licenciatura-en-sistemas")
        return pd.DataFrame()


class LI(Plan):

    # plan.insert(loc=0, column='Código', value=[self.get_cods(row) for row in plan.Nombre])

    def __init__(self, fecha):
        super().__init__(f"licenciatura-en-informatica-plan-{fecha}")

    def plan(self) -> pd.DataFrame:
        plan = self._get_plan()
        tesis, opt = self.get_indexs(plan, ['0I503', '-'])
        plan.loc[tesis[0], 'Correlativas'] = '-'
        plan.loc[opt[0], 'Código'] = 'OP1LI'
        return plan

    def optativas(self) -> pd.DataFrame:
        return pd.DataFrame()


class APU(Plan):

    def __init__(self, fecha):
        super().__init__(f"analista-programador-universitario-plan-{fecha}")

    def plan(self) -> pd.DataFrame:
        plan = self._get_plan()[:23]
        return plan

    def optativas(self) -> pd.DataFrame:
        plan = self._get_plan()
        end = self.get_index_of_string(plan, 'ELEGIR')[0]
        plan = plan[end + 1:]
        plan['Area'] = 'Optativa'
        return plan


class ATIC(Plan):

    def __init__(self, fecha):
        super().__init__(f"analista-en-tecnologias-de-la-informacion-y-la-comunicacion-plan-{fecha}")

    def plan(self) -> pd.DataFrame:
        plan = self._get_plan()[:22]
        plan.loc[21, 'Código'] = 'PPS'
        return plan

    def optativas(self) -> pd.DataFrame:
        plan = self._get_plan()[24:]
        sep = self.get_index_of_string(plan, 'ORIENTACIÓN') + [len(plan) + 24]
        for i, name in enumerate(sep):
            try:
                plan.loc[sep[i]:sep[i + 1], 'SubArea'] = plan['Código'][name][11:]
                plan.loc[sep[i]:sep[i + 1], 'Area'] = "Optativa"
            except KeyError:
                pass
        plan.drop(axis=0, labels=sep[:-1], inplace=True)
        return plan
