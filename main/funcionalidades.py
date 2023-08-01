from .models import Todas
import datetime
def get_materias_proximo():
    headers = ['codigo', 'nombre', 'correlativas',
               'area', 'subarea', 'year', 'semestre']
    cursadas = Todas.objects.filter(cursada=True).values_list(headers[0],
                                                              flat=True)
    plan_estudio = Todas.objects.all().values_list(headers[0], headers[2])
    # Me quedo con las materias que tienen las correlativas aprobadas
    correlativas_apro = [materia
                         for materia, correlativas in plan_estudio
                         if
                         all(map(lambda cod: True if cod in cursadas else False,
                                 correlativas.split(', ')))]
    # Filtro las materias que tienen correlativas y ya están cursadas aprobadas
    correlativas_apro = list(
        filter(lambda materia: materia not in cursadas, correlativas_apro))
    # Calculo el semestre actual
    mes_act = datetime.date.today().month
    semestre_prox = str(float(2 if mes_act > 3 & mes_act < 8 else 1))

    materias = Todas.objects.filter(codigo__in=correlativas_apro,
                                    semestre__exact=semestre_prox).values(
        *headers)

    # Devuelvo las tuplas que son del próximo semestre y tienen las correlativas
    # aprobadas.
    return materias, headers