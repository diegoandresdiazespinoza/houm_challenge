#Documentación: Solución a [Houm Challenge](houm_challenge.md)

## Diseño
###### Supuestos 
- El dispositivo móvil del Houmer genera las coordenadas (latitud, longitud) y una fecha con tiempo que envía cada cierto tiempo a la API. La fecha se genera en el dispositivo.
- El Houmer debe existir para enviar una posición.
- Una propiedad (real state) queda determinada unívocamente por sus coordenadas (latitud, longitud). No existen dos propiedades con las mismas coordenadas.
- Cuando un Houmer visita una propiedad, indica mediante el móvil que inicia su visita y al terminar indica el término. Con esto se generan los datos para ser enviados a la API; fecha de inicio y fecha de término se generan en el móvil. Mientras el Houmer está visitando una propiedad no se envían datos de su posición (sólo por simplicidad para hacer los cálculos de velocidad y tiempos entre momentos más simples).
- Por simplicidad no se considera el caso que un Houmer pueda visitar más de una propiedad en una misma ventana de tiempo.
- Por simplicidad no se envían dos posiciones de un Houmer iguales para tiempos iguales. Es decir, las posiciones se envían desde el móvil cuando existen cambios de posición.
- La velocidad está en unidades de Km/H.
- Para la distancia entre posiciones se utiliza la función de distancia [Haversine](https://pypi.org/project/haversine/).
- Para todas las fechas se asume UTC.
- Un momento se considera como el intervalo de tiempo que transcurre entre dos posiciones distintas del Houmer.
- Para el cálculo de los momentos se considera que dos momentos son aquellos que están más cercas en términos de tiempo. 
- Por simplicidad, para el cálculo de las velocidades se consideran sólo las posiciones (no las visitas a las propiedades).
![Diagrama para algunos supuestos](./drawings/supuestos.png)

######Arquitectura
Se considera una arquitectura simple con un servidor que expone rutas (end-points) y que internamente se conecta con una base de datos.
El servidor es stateless por lo que no guarda información de sesiones, ni cookies, ni estados particulares de las peticiones mismas; cualquier persistencia
se hace al modelo de datos expuesto en la base de datos.
![Diagrama para algunos supuestos](./drawings/arquitectura.png)
######Tech stack
- El lenguaje de programación es Python 3.10.
- Para el servidor se utiliza el web framework Flask.
- Para la base de datos se utiliza Mysql 8.0.29.
- Las librerías utilizadas se pueden ver en [requirements](./requirements.txt)
- Se utiliza un ORM mediante SQLAlchemy; la creación de las tablas se hace automáticamente.
######Diagrama Entidad-Relación
Se considera el siguiente diagrama entidad relación para la base de datos.
![Diagrama entidad relación](./drawings/er.png)
- Un Houmer puede tener asociadas cero o más posiciones (houmer_position).
- Una visita está asociada a una propiedad (real_state) y un Houmer en cierto intervalo de tiempo.
- Una propiedad queda determinada por su latitud y longitud.
- Un Houmer puede tener cero o más visitas (houmer_visit_real_state).
######Control de versiones
Se utiliza GIT con un marco de trabajo [GitFlow](https://www.gitkraken.com/learn/git/git-flow) simplificado:
- Los nombres de ramas se separan en feature/ release/ (por el momento no existen hotfix)
- La rama develop es la rama main (por simplicidad).
- No se utilizaron tags (por simplicidad).

######Estructura de directorios
La estructura de directorios es la siguiente:
![Diagrama entidad relación](./drawings/estructura_directorios.png)
- config.py: mantiene configuración para ambientes: development, testing y productivo.
- main.py: permite correr el servidor Flask.
- requirements.txt: archivo con las librerías y sus versiones utilizadas.
- __init__.py: inicialización de la base de datos, la aplicación flask con sus configuraciones.
- routes.py: contiene todas las rutas o end-points de la API.
- models.py: contiene todos los modelos para ser usados como ORM mediante SQLAlchemy.
- drawings: archivos de imágenes para README.md
- houm_challenge.md: archivo que contiene en markdown las instrucciones del challenge.


##Base de datos
Se utiliza base de datos relacional considerando que el problema supone relaciones intrínsecas
entre los Houmers y las propiedades (visitas y posiciones). 

##Correr en local

##Seguridad


##Escalabilidad


##Observabilidad