from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('<str:seccion>/', views.tabla, name='tabla'),
    path('update_forms/<str:key>', views.settings, name='update_forms')
]
