from django.db import models
from django.contrib.auth.models import User

class Genero(models.Model):
    gen_id = models.AutoField(primary_key=True, verbose_name= 'ID')
    gen_descripcion = models.CharField(max_length=100, verbose_name= 'Descripción')

    class Meta:
        db_table = 'Genero'
        verbose_name = 'Género'
        verbose_name_plural= 'Géneros'

    def __str__(self):
        return self.gen_descripcion


class Libro(models.Model):
    lib_id = models.AutoField(primary_key=True, verbose_name= 'ID')
    lib_titulo = models.CharField(max_length=200, verbose_name= 'Título')
    lib_autor = models.CharField(max_length=200, verbose_name= 'Autor')
    lib_anio = models.CharField(max_length=4, verbose_name= 'Año')
    lib_cantidad = models.IntegerField(verbose_name='Cantidad Disponible')

    lib_gen = models.ForeignKey(
        Genero,
        on_delete=models.PROTECT,
        db_column='lib_gen_id',
        related_name='libros',
        verbose_name= 'Género',
    )

    class Meta:
        db_table = 'Libros'
        verbose_name = 'Libro'
        verbose_name_plural= 'Libros'

    def __str__(self):
        return self.lib_titulo


class Prestacion(models.Model):
    pre_id = models.AutoField(
        primary_key=True,
        verbose_name='ID'
    )

    pre_usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='prestaciones',
        verbose_name='Usuario'
    )

    pre_lib = models.ForeignKey(
        Libro,
        on_delete=models.PROTECT,
        db_column='pre_lib_id',
        related_name='prestaciones',
        verbose_name='Libro'
    )

    pre_cantidad = models.PositiveIntegerField(
        verbose_name='Cantidad'
    )

    pre_fechaprest = models.DateField(
        verbose_name='Fecha de préstamo'
    )

    pre_fechasalida = models.DateField(
        verbose_name='Fecha de salida'
    )

    def __str__(self):
        cantidad_devuelta = sum(
            devolucion.dev_cantidad
            for devolucion in self.devoluciones.all()
        )

        pendiente = self.pre_cantidad - cantidad_devuelta

        return (
            f'{self.pre_lib.lib_titulo} - '
            f'Prestado: {self.pre_cantidad} - '
            f'Pendiente: {pendiente}'
        )

class Devolucion(models.Model):
    dev_id = models.AutoField(
        primary_key=True,
        verbose_name='ID'
    )

    dev_prestacion = models.ForeignKey(
        Prestacion,
        on_delete=models.PROTECT,
        related_name='devoluciones',
        verbose_name='Prestación'
    )

    dev_cantidad = models.PositiveIntegerField(
        verbose_name='Cantidad devuelta'
    )

    dev_fecha = models.DateField(
        auto_now_add=True,
        verbose_name='Fecha de devolución'
    )

    class Meta:
        db_table = 'Devoluciones'
        verbose_name = 'Devolución'
        verbose_name_plural = 'Devoluciones'

    def __str__(self):
        return (
            f'Devolución {self.dev_id} - '
            f'{self.dev_prestacion.pre_lib.lib_titulo} - '
            f'{self.dev_cantidad} unidad(es)'
        )
# Create your models here.
