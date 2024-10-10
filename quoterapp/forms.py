from django import forms

class CotizacionForm(forms.Form):
    nombre_cliente = forms.CharField(label='Nombre del Cliente', max_length=255)
    rut_cliente = forms.CharField(label='RUT', max_length=255)
    marca_vehiculo = forms.CharField(label='Marca del Vehículo', max_length=255)
    modelo_vehiculo = forms.CharField(label='Modelo del Vehículo', max_length=255)
    license_plate = forms.CharField(label='Patente del Vehículo', max_length=255)
    año_vehiculo = forms.IntegerField(label='Año del Vehículo')
    
    #uso_vehiculo = forms.CharField(label='Uso del Vehículo', max_length=255)
    #tipo_vehiculo = forms.CharField(label='Tipo de Vehículo', max_length=255)
    