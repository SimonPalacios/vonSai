from .models import Todas
import datetime


def get_materias_proximo():
    headers = ['codigo', 'nombre', 'correlativas',
               'area', 'subarea', 'year', 'semestre']
    # Calculo el próximo semestre
    mes_act = datetime.date.today().month
    semestre_prox = str(float(2 if mes_act > 3 & mes_act < 8 else 1))
    # Codigos de Materias que tienen cursada aprobada
    cursadas = Todas.aprobadas.values_list(headers[0], flat=True)
    # Códigos y Correlativas de materias que son del próximo semestre y no tienen cursada aprobada
    plan_estudio = (Todas.objects
                    .filter(semestre__exact=semestre_prox, cursada=False)
                    .values_list(headers[0], headers[2]))
    # Me quedo con las materias que tienen las correlativas aprobadas
    correlativas_apro = [materia
                         for materia, correlativas in plan_estudio
                         if
                         all(map(lambda cod: True if cod in cursadas else False,
                                 correlativas.split(', ')))]

    materias = Todas.objects.filter(codigo__in=correlativas_apro,
                                    semestre__exact=semestre_prox).values(
        *headers)

    # Devuelvo las tuplas que son del próximo semestre y tienen las correlativas
    # aprobadas.
    return materias, headers
