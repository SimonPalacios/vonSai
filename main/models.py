from typing import List

from django.db import models


class TodasCursando(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(cursando=True)


class TodasAprobadas(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(cursada=True)


class Todas(models.Model):
    codigo = models.TextField(primary_key=True, unique=True, db_column='Codigo')
    nombre = models.TextField(db_column='Nombre', max_length=90)
    correlativas = models.TextField(db_column='Correlativas', default='-', blank=True,
                                    null=True, max_length=50)
    area = models.TextField(db_column='Area', default='-', blank=True,
                            null=True, max_length=50)
    subarea = models.TextField(db_column='SubArea', default='-', blank=True,
                               null=True, max_length=50)
    year = models.IntegerField(db_column='Year', default='-', blank=True,
                               null=True)
    semestre = models.TextField(db_column='Semestre', blank=True,
                                null=True)
    cursando = models.BooleanField(db_column='Cursando')
    cursada = models.BooleanField(db_column='Cursada')
    final = models.BooleanField(db_column='Final')
    objects = models.Manager()
    aprobadas = TodasAprobadas()
    cursada_actual = TodasCursando()

    class Meta:
        managed = False
        db_table = 'todas'


class PlanEstudioMaterias(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(codigo__isnull=False)


class PlanEstudio(models.Model):
    nombre: str
    codigo = models.TextField(db_column="ATIC")
    materias = PlanEstudioMaterias()

    def change_plan(self):
        self.codigo = models.TextField(db_column=self.nombre)

    class Meta:
        managed = False
        db_table = 'planes'
