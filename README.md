# GPTSeguros

Durante este proyecto ire desarrollando el trabajo a realizar con GPT-Seguros.
El trabajo consiste en realizar un 'cotizador' automatico de paginas webs con Python.
Se hacen uso de 8 diferentes paginas de seguros.

* https://portalcorredores.mapfre.cl/
* https://www.hdicorredores.cl/homeCorredores.asp
* https://oficinavirtual.bciseguros.cl/Home/LinkLogin?ReturnUrl=%2fprincipal%2fprincipal
* https://seguros.sura.cl/acceso/corredor
* https://portal.fidseguros.cl/Fidnet_UI/Logins.aspx?Type=2
* https://sgi.rentanacional.cl/
* https://www.ant.cl/portal/account/login
* https://apps4.realechile.cl/portalCorredores/login

### Estructtura

El trabajo contiene carpetas de trabajo **selenium** y **request**. Ademas contiene la carpeta *utils* donde se encuentran archivos utiles para el proyecto tales como 'requirements' o 'graph' que son codigo basales inicialmente. **gptsite** viene respecto a lo necesario para django junto con 'manage.py'.

### Version 1
Se crea una interfaz grafica con la que es posible interactuar para obtener informacion de los PDF's.
* Autos de uso particular usados
* input: data_cliente = "patente","marca","modelo","año","nombre_asegurado","rut"
* output: pdf's con cotizaciones

#### USO:
- correr 'cotizador.py' para ejecutar cotizacion por consola.
- 'themes.py' corresponde a la interfaz grafica del cotizador, realiza cotizacion.
- requirements.txt corresponde a las intalaciones necesarias para correr los codigos anteriores.
- test.ipynb son pruebas para revisar el cotizador compañia a compañia.
- En la carpeta build se encuentra el cotizador empaquetado como ejecutable.

#### Probelmas

* BCI tuvo problemas al considerar modelos.
* Sura tuvo problemas al reconocer la Marca.
* HDI tuvo problemas al seleccionar (necesita un breve tiempo de presion), ademas problemas de la pagina.
* Se quedan algunos archivos en la carpeta de descarga.
* Aun el programa es muy lento. 
* Revisar otros programas que no sean python.
* Que ocurre con la migracion del ejecutable.
* aumentar los tiempos de espera.
* no carga bien la pagina del cotizador.

#### Cotizaciones
Actualmente solo funciona la descarga automatica del archivo PDF para: BCI, Renta, Sura, FID .

* Mapfre tiene un detectador anti-automatizadores
* HDI tuvo una caida actualemnte.
* ANS se descarto.

Al hacer las conexiones con la interfaz grafica hay problemas para la realizacion en orden; algunas soluciones son: boton que ejecute por modelo usando la informacion global.

*Por realizar*:
* Reale: Hay que hacerlo desde 0
* Zurich: Tiene precios atractivos

### Version 2
Traspasar la idea realizada en la V1 a una aplicacion web atraves de django. 

