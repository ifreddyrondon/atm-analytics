# atm-analytics

# Dependencias #
## Dependencias del sistema ##
* Python 2.7
* pip
```
#!bash

python get-pip.py
```
* Postgresql > 9.3
* git
* wkhtmltopdf

## Dependencias del proyecto ##
* Django==1.8.3
* django-grappelli==2.7.3
* django-widget-tweaks==1.4.1
* pdfkit==0.5.0
* Pillow==3.1.0
* psycopg2==2.6.1
* PyPDF2==1.25.1
* python-dateutil==2.5.2
* python-evtx==0.3.2
* six==1.10.0
* xmltodict==0.9.2

# Proceso de instalación #
## Instalar Dependencias del sistema ##
1. Ingresar a la instancia de AWS con las credenciales suministrada en la sección de descargas de este repositorio 
2. Instalar las dependencias del sistema
## Instalar dependencias del proyecto ##
1. Es recomendable instalar un entorno virtual a través de **virtualenv** (instalar con pip como global) 
2. Activar entorno virtual
3. Clonar repositorio 
4. Instalar dependencias del proyecto
```
#!bash

pip install -r requirements/production.txt
```
## Creación de la Base de datos con PosgreSQL ##
1. Creación de usuario
```
#!bash

sudo -u postgres createuser #NOMBRE_DE_USUARIO
```
2. Permisos del nuevo usuario: Ingresando al shell de postgres 
```
#!bash

psql
ALTER ROLE #NOMBRE_DE_USUARIO SUPERUSER;
\q
```
3. Creación de base de datos

```
#!bash

sudo -u postgres createdb -O #NOMBRE_DE_USUARIO #NOMBRE_DE_BASE_DE_DATOS
```
## Instalación y configuración de Django ##

1. En la carpeta **/atm_analytics/settings/** crear un archivo **local.py** y copiar

```
#!python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '#NOMBRE_DE_BASE_DE_DATOS',
        'USER': '#NOMBRE_DE_USUARIO',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '#PUERTO_DONDE_ESTA_CORRIENDO_POSTGRE_SQL',
    }
}
```

2. Correr migraciones: En la carpeta **/atm_analytics/** correr el comando

```
#!bash

python manage.py migrate
```

## Insertar un nuevo idioma ##

Para agregar un nuevo idioma es necesario crear los archivos del lenguaje para eso se utiliza el comando 
```
#!bash

python manage.py makemessages -l #NOMBRE_LOCAL_DEL_IDIOMA
```

Los siguientes archivos de idiomas ya están creados:

* de (Alemán)
* es (Español)
* fr (Frances)
* pt (Portugués)
* ru (Ruso)

### Agregar traducciones a alguno de los idiomas anteriores ###
1. Actualizar los archivos de idiomas con los últimos textos de la aplicación
```
#!bash

python manage.py makemessages
```

2. Agregar las traducciones, para esto se edita el archivo en la ruta **/atm_analytics/locale/#NOMBRE_LOCAL_DEL_IDIOMA/LC_MESSAGES/django.po**

Este archivo contiene las traducciones de cada linea de la siguiente manera:

* **msgid** es el texto a ser traducido, que aparece en el archivo fuente. **NO CAMBIARLO**.
* **msgstr** es donde se coloca la traducción especifica del lenguaje. Comienza vacío, por lo tanto es responsabilidad del encargado de llenarlo.

Por conveniencia, cada mensaje incluye en forma de comentario una linea con el prefijo # localizada sobre el msgid, contiene el nombre del archivo y el número de linea.

Ejemplo:
```
#!bash
#: path/to/python/module.py:23
msgid "Welcome to my site."
msgstr "Bienvenido a mi sitio"
```

Para más ejemplos revisar el archivo **/atm_analytics/locale/es/LC_MESSAGES/django.po** con las traducciones de Ingles a Español.

Después de crear o cada vez que se edita el archivo de idioma es necesario compilarlo a una forma más eficiente. Para eso utilizamos el comando
```
#!bash
python manage.py compilemessages
```

### Activar o desactivar algún idioma ya existente ###
Para activar un idioma existente es necesario agregar a la tupla **LANGUAGES** dentro del archivo **/atm_analytics/settings/base.py** el #NOMBRE_LOCAL_DEL_IDIOMA y como desea que aparezca en el menú 
```
#!python
LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
```

# Estructura de la base de datos #

## Diagrama Entidad - Relación ##
![ERD.png](https://bitbucket.org/repo/GozMA6/images/2449767825-ERD.png)


## Crear nuevos usuarios Manager y analista ##

### Manager ###
Para crear nuevos usuarios Manager es necesario entrar a la interfaz del administrador y crear una compañía o ingresar una compañía ya creada, luego en la sección de usuarios se debe seleccionar un usuario ya creado de django o crear uno nuevo y seleccionar el cargo manager.

### Analista ###
Los analistas pueden ser creados por los administradores de la misma forma que los manager pero seleccionando el cargo de analista o en la interfaz de los managers se selecciona **Agregar Usuario** y se llenan los campos necesarios.

## Inserción de datos para software ##

### Casos ###
Los datos son ingresados al sistemas a través de casos que pueden ser creados por los analistas. Para crear un caso es necesario especificar el nombre del caso, fecha de creación, monto faltante, divisa, importancia y estado del caso. Cada caso pertenece a un banco por lo tanto también se debe seleccionar al momento de crear el caso y especificar la cantidad de ATMs que se quieren detallar en el caso.

Por cada ATM se debe seleccionar el hardware, software y sistema operativo que operan en ellos, si el analista posee los manuales del ATM se pueden seleccionar para facilitar el proceso de análisis, si el analista tiene a su disposición los eventos de Windows también se debe seleccionar. Es necesario especificar el nombre de la persona que facilita los archivos XFS y ademas seleccionar todos los archivos XFS que se quieren analizar para el ATM. Por ultimo cada ATM debe poseer una dirección previamente creada por el manager o el administrador.

### Direcciones de los ATM ###

Las direcciones pueden ser creadas en la interfaz del administrador en la sección de direcciones de los ATMs dentro de cada compañía y también puede ser creadas por los managers en la sección de configuración especificándolas una a una o subiendo un archivos csv donde la primera posición de cada linea corresponde a la dirección.

### Archivos de reposición de efectivo ###

Este archivo es subido por el manager de cada compañía debe tener la extensión .csv y ademas contener los siguientes campos: 

- Columna A: Nombre del banco
- Columna B: Dirección del atm (igual a la especificada en las direcciones de los ATM ya creadas)
- Columna C: fecha en formato DD/MM/YYYY HH:MM

Se pueden agregar nuevas columnas para posterior análisis pero estas son las únicas tomadas en cuenta hasta el momento.

### Asignación de culpabilidad ###

Para asignar culpabilidad a los errores es necesario entrar a la interfaz del administrador y crear o ingresar a un error ya sea XFS o de EventViewer, luego en la sección de culpabilidad se especifica quien es el culpable entre usuario, banco, transvalores o anónimo.

## Documentación  del proceso de análisis ##

El de análisis consta de varios procesos, cada proceso es aplicado a cada ATM que se especificó en el caso, luego se envían los datos a la plantilla de análisis para ser renderizada en el cliente.

### Proceso de análisis de Microsoft events ###

Si el ATM no posee Microsoft events se salta este paso. Este proceso consta de encontrar las fecha mínima y máxima dentro de los eventos de Microsoft para luego ser pasados a la vista, dichas fechas son necesarias porque los eventos de Microsoft no están activos por omisión en la vista si no que hay que seleccionar un fecha comprendida entre el rango fecha mínima y máxima.

### Proceso de análisis de archivos XFS ###

Cada archivo XFS de cada ATM es analizado por un parser parametrizado por un formato previamente creado por un manager. Este parser toma el contenido de cada archivo y los separa en grupos, esta separación ocurre partiendo todo el contenido con un separador de grupo especificado en el formato, luego dentro de cada grupo se buscan los siguientes campos:

* **fecha** (especificada en el formato), si no existe fecha se pasa al siguiente grupo ya que es necesaria.
* **monto** (especificado en el formato), no es requerido ya que pueden existir eventos que no necesariamente llevan fecha.
* **eventos** (especificados en el formato), existen 3 tipos de eventos, eventos críticos, importantes y sin errores. 

Es necesario encontrar un solo evento para pasar al siguiente grupo. Los eventos se buscan por prioridad de críticos, importantes y sin errores lo que significa que aunque exista mas de un evento en un grupo solo encontrara el evento que se haya encontrado primero dependiendo su la prioridad.

### Proceso de análisis de eventos de reposición de efectivo ###

Si el ATM no posee eventos de reposición se salta este paso. Dado que estos eventos ya fueron subidos por el manager solo se busca en base de datos estos eventos para el ATM en especifico.

## Documentación del proceso de graficado

Se utilizan varias bibliotecas Javascript para el proceso de graficado. 

* **D3.js**: es utilizada para dibujar los graficos dentro de la página. [https://d3js.org/](https://d3js.org/)
* **Crossfilter**: es utilizada para realizar el proceso de filtrado de los datos creando dimensiones en las que se pueden realizar consultas dependiendo del tipo de dimensión. [http://square.github.io/crossfilter/](http://square.github.io/crossfilter/)
* **dc.js**: Esta biblioteca se integra con D3.js y crossfilter para construir gráficos ya definidos en su API. [https://dc-js.github.io/dc.js/](https://dc-js.github.io/dc.js/)
* **vis.js - timeline **: Esta biblioteca es utilizada para construir el timeline de datos. [http://visjs.org/docs/timeline/](http://visjs.org/docs/timeline/)

El contenido de cada elemento en el timeline es especificado por la clave **content** dentro de los objetos pasados al timeline por lo tanto para modificar esta clave solo es necesario especificar que contenido se desea mostrar. Por ejemplo si se quiere mostrar el identificador del evento ya guardado en el backend es necesario hacer la búsqueda de dicho identificador antes de pasarlo a la plantilla luego agregarla en el diccionario de cada evento y al llegar a la plantilla recorrer la lista de los objetos para reemplazar la clave content por la los datos agregados en el diccionario que contiene el identificador del error.

## Asignación del porcentaje de culpabilidad ##

Para hacer esto es necesario obtener por cada evento XFS de cada ATM su match con los campos de culpabilidad para el XFS en el backend luego pasar esos datos a la plantilla donde se deben obtener los datos mostrados en la ventana del timeline y sumar la cantidad cada vez que se mueva el timeline, sumar todos los eventos con un mismo culpable multiplicarlos por 100 y se dividirlos por el total de eventos.

## Dirección de archivos subidos ##

- Manuales pdf **/atm_analytics/media/errors_manual/FECHA DE SUBIDA/**
- Archivos de reposición, No se guardan ya que son guardados directamente en base de datos
- Archivos de journal **/atm_analytics/media/atm/models.py/FECHA DE SUBIDA/**
- Archivos de windows event viewer **/atm_analytics/media/atm/microsoft_event_viewer/FECHA DE SUBIDA/**
- Archivos extras **/atm_analytics/media/atm/other_log/FECHA DE SUBIDA/**
