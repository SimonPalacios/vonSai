from typing import List
from django import forms
import base
from .funcionalidades import get_materias_proximo


def get_planes() -> List[tuple]:
    dict_planes = base.get(f"select name from pragma_table_info('planes')")['name']
    dict_planes.pop(0)
    return [(plan, plan) for plan in dict_planes.values()]


class PlanChoiceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PlanChoiceForm, self).__init__(*args, **kwargs)
        self.fields['plan'] = forms.ChoiceField(choices=get_planes())


class CursandoForm(forms.Form):
    materias, headers = get_materias_proximo()
    opciones = materias.values_list('codigo', 'nombre')
    codigo = forms.ChoiceField(choices=opciones,
                               widget=forms.SelectMultiple(attrs={'class': 'dropdown-select'}),
                               label="Selecciona")

    def clean_codigo(self):
        choices = self.cleaned_data.get('codigo', [])
        if not choices:
            raise forms.ValidationError("Campos minimo")
        return choices


class UploadFileForm(forms.Form):
    archivo = forms.FileField(widget=forms.FileInput(attrs={'class': "form-control input-lg",
                                                            'type': "file",
                                                            'name': "inputfile",
                                                            'enctype': "multipart/form-data"
                                                            }))

    # class Meta:
    #
    #     widgets = {
    #         'archivo': forms.FileInput(attrs={'class': "form-control input-lg",
    #                                           'name': "inputfile",
    #                                           'type': "file"})}
