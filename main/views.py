from django.http import HttpResponse
from django.shortcuts import render

from historiaAcademica import modelar
from . import funcionalidades
from .models import Todas, PlanEstudio
from .forms import PlanChoiceForm, UploadFileForm, CursandoForm


def get_headers():
    headers = ['codigo', 'nombre', 'correlativas', 'area', 'subarea', 'year',
               'semestre']
    return headers


def inicio(request):
    return render(request, 'background.html')


def tabla(request, seccion=None):
    tabla_info = {'aprobadas': get_aprobadas(), 'plan': get_plan(),
                  'todas': get_todas(), 'cursando': get_cursando(),
                  'proximo': get_materias_proximo()}
    try:
        return render(request, 'table.html', tabla_info[seccion])
    except KeyError:
        return render(request, 'background.html')


def get_todas():
    headers = get_headers()
    materias = list(Todas.objects.values(*headers))
    headers = [head.capitalize() for head in headers]
    headers[-2] = 'Año'
    return {'columnas': headers,
            'materias': materias}


def get_plan():
    return {'columnas': get_headers(),
            'materias': list(Todas.objects.values())}


def get_materias_proximo():
    materias, headers = funcionalidades.get_materias_proximo()
    headers[-2] = 'Año'
    return {'columnas': list(map(lambda x: x.capitalize(), headers)),
            'materias': materias}


def get_cursando():
    headers = ['codigo', 'nombre', 'year']
    materias = Todas.objects.filter(cursando=True).values(*headers)
    headers = [head.capitalize() for head in headers]
    headers[2] = "Año"
    return {'columnas': headers,
            'materias': materias}


def get_aprobadas():
    headers = ['codigo', 'nombre', 'cursada', 'final']
    # Obtengo todas las materias que tienen cursadas aprobadas.
    cursadas = list(Todas.objects.filter(cursada=True).values(*headers))
    for value in cursadas:
        value['cursada'] = 'A' if value['cursada'] else '-'
        value['final'] = 'A' if value['final'] else '-'
    headers = list(map(lambda x: x.capitalize(), headers))
    return {'columnas': headers,
            'materias': cursadas}


def cursada(request):
    if request.method == 'POST':
        choices = dict(request.POST)['codigo'][:-1]
        if choices:
            Todas.objects.filter(codigo__in=choices).update(cursando=True)
            return HttpResponse(
                status=204,
            )
    else:
        return {'form': CursandoForm(),
                'title': "Elegir Cursadas Actuales"}


def historia(request):
    if request.method == "POST":
        # Obtengo el dataframe del archivo con cursadas aprobadas y finales

        print(request.FILES)
        df = modelar(request.FILES['archivo'])
        df = df.to_dict(orient='index')
        # Pongo todas las cursadas y finales en False
        Todas.objects.all().update(cursada=False, final=False)
        # Por cada item del dataframe busco en la db y actualizo
        for key, values in df.items():
            Todas.objects.filter(codigo=key).update(cursada=values['Cursadas'],
                                                    final=values['Finales'])
        return HttpResponse(
            status=204,
        )
    else:
        form = UploadFileForm()
        # print("FORM", form.fields['archivo'].widget.attrs)
        return {'form': form,
                'title': "Cargar Historia Académica"}


def planes(request):
    if request.method == 'POST':
        HttpResponse(
            status=204,
        )
    else:
        return {'form': PlanChoiceForm(),
                'title': "Cambiar Plan Estudio"}


def settings(request, key=None):
    forms = {'historia': historia,
             'cursando': cursada,
             'plan': planes}

    content = forms[key](request)
    if request.method == "GET":
        return render(request, 'forms.html', context=content)
    else:
        return content
