from django import forms
from .models import Prestacion, Devolucion, Libro

class LibroModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.lib_titulo} - Stock: {obj.lib_cantidad}'
class PrestacionForm(forms.ModelForm):
    pre_lib = LibroModelChoiceField(
        queryset=Libro.objects.filter(lib_cantidad__gt=0),
        label='Libro'
    )

    class Meta:
        model = Prestacion

        fields = [
            'pre_lib',
            'pre_cantidad',
            'pre_fechaprest',
            'pre_fechasalida',
        ]

        labels = {
            'pre_cantidad': 'Cantidad',
            'pre_fechaprest': 'Fecha de préstamo',
            'pre_fechasalida': 'Fecha de salida',
        }

        widgets = {
            'pre_cantidad': forms.NumberInput(
                attrs={'min': 1}
            ),
            'pre_fechaprest': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'pre_fechasalida': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

class DevolucionForm(forms.ModelForm):
    class Meta:
        model = Devolucion

        fields = [
            'dev_prestacion',
            'dev_cantidad',
        ]

        labels = {
            'dev_prestacion': 'Prestación',
            'dev_cantidad': 'Cantidad a devolver',
        }

        widgets = {
            'dev_cantidad': forms.NumberInput(
                attrs={'min': 1}
            ),
        }

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)

        if usuario:
            prestaciones_usuario = Prestacion.objects.filter(
                pre_usuario=usuario
            )

            ids_pendientes = []

            for prestacion in prestaciones_usuario:
                cantidad_devuelta = sum(
                    devolucion.dev_cantidad
                    for devolucion in prestacion.devoluciones.all()
                )

                cantidad_pendiente = (
                    prestacion.pre_cantidad - cantidad_devuelta
                )

                if cantidad_pendiente > 0:
                    ids_pendientes.append(prestacion.pre_id)

            self.fields['dev_prestacion'].queryset = (
                Prestacion.objects.filter(
                    pre_id__in=ids_pendientes
                )
            )