from django.db import models


class Todas(models.Model):
    codigo = models.TextField(primary_key=True, db_column='Codigo')
    nombre = models.TextField(db_column='Nombre', max_length=90)
    correlativas = models.TextField(db_column='Correlativas', max_length=70,
                                    blank=True, null=True)
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

    class Meta:
        managed = False
        db_table = 'todas'


class PlanEstudio(models.Model):
    codigo = models.TextField(primary_key=True, db_column='LS')


    class Meta:
        managed = False
        db_table = 'planes'

