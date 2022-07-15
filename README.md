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

###### Arquitectura
Se considera una arquitectura simple con un servidor que expone rutas (end-points) y que internamente se conecta con una base de datos.
El servidor es stateless por lo que no guarda información de sesiones, ni cookies, ni estados particulares de las peticiones mismas; cualquier persistencia
se hace al modelo de datos expuesto en la base de datos.
![Diagrama para algunos supuestos](./drawings/arquitectura.png)
###### Tech stack
- El lenguaje de programación es Python 3.10.
- Para el servidor se utiliza el web framework Flask.
- Para la base de datos se utiliza Mysql 8.0.29.
- Las librerías utilizadas se pueden ver en [requirements](./requirements.txt)
- Se utiliza un ORM mediante SQLAlchemy; la creación de las tablas se hace automáticamente.
- Se utiliza ambiente Windows (aunque las instrucciones deberían funcionar en Linux).
- Se utiliza para test unitarios unittest de pytest
- Se prueba en windows usando WSGI waitress
###### Diagrama Entidad-Relación
Se considera el siguiente diagrama entidad relación para la base de datos.
![Diagrama entidad relación](./drawings/er.png)
- Un Houmer puede tener asociadas cero o más posiciones (houmer_position).
- Una visita está asociada a una propiedad (real_state) y un Houmer en cierto intervalo de tiempo.
- Una propiedad queda determinada por su latitud y longitud.
- Un Houmer puede tener cero o más visitas (houmer_visit_real_state).
###### Control de versiones
Se utiliza GIT con un marco de trabajo [GitFlow](https://www.gitkraken.com/learn/git/git-flow) simplificado:
- Los nombres de ramas se separan en feature/ release/ (por el momento no existen hotfix)
- La rama develop es la rama main (por simplicidad).
- No se utilizaron tags (por simplicidad).

###### Estructura de directorios
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
- testing incluye los test unitarios utilizando unittest.


## Base de datos
Se utiliza base de datos relacional considerando que el problema supone relaciones intrínsecas
entre los Houmers y las propiedades (visitas y posiciones). 

## Ejecución en local

ATENCIÓN: Las tablas necesarias se crean automáticamente al inicio (en caso de no estar creadas) dado
que se utiliza SQLAlchemy como ORM. Crearlas manualmente puede causar errores en la ejecución. 
Los schemas de las bases correspondientes a los distintos ambientes deben crearse manualmente.
Los usuarios y permisos de los schemas en la base de datos deben crearse manualmente. 


### Configuración y ejecución en Windows
- ``` pip3 install -r requirements.txt ``` para instalar dependencias de librerías
- ``` set HOUM_DEVELOPMENT_DATABASE_URI='mysql+pymysql://<development_user>:<development_user_password>@localhost:<port>/development' ``` Para correr en modo Debugger sin WSGI (usando correspondiente schema, usuario, password y puerto para cada ambiente)
- ``` set HOUM_TESTING_DATABASE_URI='mysql+pymysql://<testing_user>:<testing_user_password>@localhost:<port>/testing' ``` Para correr en modo Testing sin WSGI (usando correspondiente schema, usuario, password y puerto para cada ambiente)
- ``` set HOUM_PRODUCTIN_DATABASE_URI='mysql+pymysql://<testing_user>:<production_user_password>@localhost:<port>/production' ``` Para correr en modo Producción sin WSGI (usando correspondiente schema, usuario, password y puerto para cada ambiente)
- ``` set API_SECRET_KEY="development"```
- ``` set APP_ENVIRONMENT="[<development>|<testing>|<production>]"``` <...> dependiendo del ambiente a correr. 
- ``` python3 main.py ``` dentro del directorio del proyecto para correr sin WSGI (no recomendado para ambientes productivos)
- Para correr utilizando WSGI (en este caso waitress para Windows)
- ``` pip3 install waitress```
- ``` waitress-serve --listen=localhost:5000 main:app ```
### Configuración y ejecución Linux (experimental, dado que todo fue probado en Windows)
- ``` pip3 install -r requirements.txt ``` para instalar dependencias de librerías
- ``` export HOUM_DEVELOPMENT_DATABASE_URI='mysql+pymysql://<development_user>:<development_user_password>@localhost:<port>/development' ``` Para correr en modo Debugger sin WSGI (usando correspondiente schema, usuario, password y puerto para cada ambiente)
- ``` export HOUM_TESTING_DATABASE_URI='mysql+pymysql://<testing_user>:<testing_user_password>@localhost:<port>/testing' ``` Para correr en modo Testing sin WSGI (usando correspondiente schema, usuario, password y puerto para cada ambiente)
- ``` export HOUM_PRODUCTIN_DATABASE_URI='mysql+pymysql://<testing_user>:<production_user_password>@localhost:<port>/production' ``` Para correr en modo Producción sin WSGI (usando correspondiente schema, usuario, password y puerto para cada ambiente)
- ``` export API_SECRET_KEY="development"```
- ``` export APP_ENVIRONMENT="[<development>|<testing>|<production>]"``` <...> dependiendo del ambiente a correr. 
- ``` python3 main.py ``` dentro del directorio del proyecto para correr sin WSGI (no recomendado para ambientes productivos)
- - Para correr utilizando WSGI (en este caso waitress para Gunicorn)
- ``` pip3 install gunicorn```
- ``` gunicorn --bind 0.0.0.0:5000 main:app ```

### Rutas (end-points)
La API utiliza una autentificación simple usando JWT para Python. Cada llamada debe entregar en un Header
el token de autentificación. Por simplicidad se provee un solo token que es codificado una sola vez
con un payload de ejemplo. Por simplicidad la decodificación no verifica que el payload decodificado
coincida con los datos utilizados para generar el token. Como mejora, debería existir una tabla
que registre los usuarios autorizados de la API junto con sus payloads, el token se debería generar
con esos datos y luego al pasar el token a la API se debería corroborar la codificación en la DB.
En la sección de mejoras de esta documentación se puede encontrar formas óptimas de resolver la seguridad
de las llamadas a la API (mediante OAUTH2 por ejemplo).

#### Headers

- ``` x-access-tokens :  eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZGllZ28iLCJlbWFpbCI6InRlc3QifQ.BBzMWAEaLOinBnqsiH0oWgCCQiuInqOriwgQgnMwcU8 ``` En modo productivo
el token no debería guardarse ni este README ni versionarse en el repositorio. Los tokens de acceso se deberían
generar una vez y no ser guardados en la DB (lo que se guarda es el payload decodificado). Para generar un nuevo token
se puede hacer un python con la siguiente instrucción:

``` jwt.encode(<payload>, app.config["SECRET_KEY"], algorithm='HS256') ```

Además debe indicar en el request el content type del body del request:

- ``` Content-Type: "application/json" ```

Todas las rutas siguientes deben incluir los headers anteriores en cada llamada.

#### Schemas
Todas las rutas tienen un chequeo de schemas del payload pasado como application/json en el body.
Los schemas están definidos en el archivo [config.py](./config.py). Cualquier error en el body o en el schema
devuelve un payload:
- ```{"error": "no valid payload"}``` cuando el payload no corresponde a formato Json.
- ```{"error": "invalid schema"}``` cuando el schema es inválido.

#### Rutas

###### Status
Se incluye una ruta que simplemente verifica que la API esté corriendo correctamente. Igualmente
debe incluir los headers descritos anteriormente.

- ``` http://localhost:5000/houm_challenge/status ``` Status de la API
  - body: sin body
  - response: ``` {api status ok} ``` con status code 200.
  - Por simplicidad se deja de lado un mensaje de error con status 400 ya que el WSGI debería indicarlo.
  - Ejemplo ``` curl -X POST -H 'Content-Type: application/json' -H 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZGllZ28iLCJlbWFpbCI6InRlc3QifQ.BBzMWAEaLOinBnqsiH0oWgCCQiuInqOriwgQgnMwcU8' -i http://localhost:5000/houm_challenge/status ```

###### Houmer
Permite ingresar un nuevo Houmer. Se incluye por completitud para no tener que llenar los
Houmer manualmente.

- ``` http://localhost:5000/houm_challenge/houmer ```
    - body: ```{"name": "<value>", "email":"<value>"}```
    - response: ``` {"message": "houmer inserted ok. id:<houmer_id>"} ``` houmer_id corresponde al id con el que se registró
al Houmer. Status code 200.
    - Cualquier error en el proceso responderá ```{"message": "Error"}``` status code 400.
No se envía información específica del error por seguridad.
    - Ejemplo ``` curl -X POST -H 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZGllZ28iLCJlbWFpbCI6InRlc3QifQ.BBzMWAEaLOinBnqsiH0oWgCCQiuInqOriwgQgnMwcU8' -H 'Content-Type: application/json' -i http://localhost:5000/houm_challenge/houmer --data '{"name":"Test", "email":"test@test.cl"}' ```

###### Houmer Position
Permite ingresar coordenadas de un Houmer con su determinado tiempo.

- ``` http://localhost:5000/houm_challenge/houmer/position ```
  - body: ```{"houmer_id" : <number>, "latitude": <decimal>, "longitude": <decimal>, "date" : "<YYYY-MM-DD HH:mm:SS>"}``` houmer_id corresponde al id del Houmer en la tabla houmer.
  - response: ```{"message": "houmer position inserted ok. id:<houmer_position_id>"}``` houmer_position_id es el id asignado a la nueva tupla.
  - Cualquier error en el proceso responderá ```{"message": "Error"}``` status code 400.
No se envía información específica del error por seguridad.
  - Ejemplo ``` curl -X POST -H 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZGllZ28iLCJlbWFpbCI6InRlc3QifQ.BBzMWAEaLOinBnqsiH0oWgCCQiuInqOriwgQgnMwcU8' -H 'Content-Type: application/json' -i http://localhost:5000/houm_challenge/houmer/position --data '{"houmer_id" : 1, "latitude": -70.1, "longitude": 20.2, "date" : "2022-07-14 16:40:00"}' ```

###### Houmer visita propiedad (real state)
Permite ingresar la visita de un Houmer a una propiedad.
- ``` http://localhost:5000/houm_challenge/houmer/visit ```
  - body: ```{"houmer_id": <numeric>, "real_state_id": <numeric>, "start_date": "<YYYY-MM-DD HH:mm:SS>", "end_date": "<YYYY-MM-DD HH:mm:SS>"}``` houmer_id
es el id del houmer que visita una propiedad. real_state_id es el id de una propiedad en la tabla real_state. La fecha de inicio y la 
fecha de término se calculan en la app (móvil), por esto que deben venir incluídas en el payload.
  - response: ```{"message": "houmer visit real state inserted ok. id:<houmer_visit_real_state_id>"}``` status code 200
houmer_visit_real_state_id es el id con el que ingresó la tupla.
  - Cualquier error en el proceso responderá ```{"message": "Error"}``` status code 400.
No se envía información específica del error por seguridad.
  - Ejemplo ``` curl -X POST -H 'Content-Type: application/json' -H 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZGllZ28iLCJlbWFpbCI6InRlc3QifQ.BBzMWAEaLOinBnqsiH0oWgCCQiuInqOriwgQgnMwcU8' -i http://localhost:5000/houm_challenge/houmer/visit --data '{"houmer_id": 1, "real_state_id": 1, "start_date": "2022-07-14 16:43:00", "end_date": "2022-07-14 16:53:00"}' ```

###### Coordenadas de las propiedades visitadas
Permite obtener las coordenadas de las propiedades visitadas por un Houmer y el tiempo que se quedó en cada una 
de ellas, para cierta fecha (día).

- ``` http://localhost:5000/houm_challenge/houmer/visit/coordinates ```
  - body: ```{"houmer_id":<numeric>, "date":<YYYY-MM-DD>"}``` houmer_id es el id del houmer que se 
quiere consultar. date es la fecha (día) que se quiere consultar (notar que no se debe especificar hora).
  - response: ```[{"latitude":<decimal>, "longitude":<decimal>, "spent_time":<HH:MM:SS>}]``` una lista
con las coordenadas de las propiedades y el tiempo o duración de la visita. HH es cantidad de horas (puede ser mayor a 24 aunque
no debería :) ), MM la cantidad de minutos (no necesariamente de dos cifras, porque pudo demorarse más de
2 digitos, aunque sería raro :) ) y SS cantidad de segundos. Status code 200.
  - Cualquier error en el proceso responderá ```{"message": "Error"}``` status code 400.
No se envía información específica del error por seguridad.
  - Ejemplo: ``` curl -X POST -H 'Content-Type: application/json' -H 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZGllZ28iLCJlbWFpbCI6InRlc3QifQ.BBzMWAEaLOinBnqsiH0oWgCCQiuInqOriwgQgnMwcU8' -i http://localhost:5000/houm_challenge/houmer/visit/coordinates --data '{"houmer_id":1, "date":"2022-07-14"}' ```

###### Houmer excede rapidez
Permite obtener todas las fechas (fecha y tiempo) en los que el Houmer excedió cierta rapidez.
Para esto se consideran -por simplicidad- sólo las posiciones ingresadas en la ruta de posición.
El cálculo consiste en la distancia entre los momentos (posiciones ingresadas) utilizando
la función de distancia para coordenadas gps (haversine) y la diferencia de tiempo en horas entre
cada posición.

- ``` http://localhost:5000/houm_challenge/houmer/exceeded_speed ```
  - body: ```{"houmer_id": <numeric>, "max_speed":<rapidez máxima>, "date":dia}``` houmer_id es el identificador
del Houmer, max_speed la rapidez máxima y el date el día a contemplar (día sin hora).
  - response: ```[<YYYY-MM-DD HH:mm:SS>]``` lista con las fechas (y tiempos) de la posición inicial
correspondiente a una tupla posición que se excedió el límite de velocidad.
  - Cualquier error en el proceso responderá ```{"message": "Error"}``` status code 400.
No se envía información específica del error por seguridad.
  - Ejemplo: ``` curl -X POST -H 'Content-Type: application/json' -H 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZGllZ28iLCJlbWFpbCI6InRlc3QifQ.BBzMWAEaLOinBnqsiH0oWgCCQiuInqOriwgQgnMwcU8' -i http://localhost:5000/houm_challenge/houmer/exceeded_speed --data '{"houmer_id": 1, "max_speed":100.0, "date":"2022-07-14"}' ``` 

###### Propiedades
Permite ingresar propiedades (real states) para efectos de completitud.

- ``` http://localhost:5000/houm_challenge/real_state ```
    - body: ```{"name":<string>, "latitude":<decimal>, "longitude":<decimal>}``` nombre y coordenadas
de la propiedad.
    - response: ``` {"message":"real state inserted ok. id:<real_state_id"} ``` real_state_id es el id con el que se ingresó la tupla. status 200.
  - Cualquier error en el proceso responderá ```{"message": "Error"}``` status code 400.
No se envía información específica del error por seguridad.
    - Ejemplo: ``` curl -X POST -H 'x-access-tokens: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiZGllZ28iLCJlbWFpbCI6InRlc3QifQ.BBzMWAEaLOinBnqsiH0oWgCCQiuInqOriwgQgnMwcU8' -H 'Content-Type: application/json' -i http://localhost:5000/houm_challenge/real_state --data '{"name":"test real state", "latitude":-70.1, "longitude":20.1}' ```


##Testing
Se utiliza modulo unittest. Para ejecutarlos primero debe estar corriendo el servicio (mediante alguno 
de los métodos mencionados):

``` python3 -m unittest discover ``` dentro del directorio testing.


## Posibles mejoras
Por simplicidad y para enfocarse en la solución de los requerimientos se tomaron ciertas decisiones y algunas
concesiones. A continuación se detallan algunas mejoras que podrían haberse introducido:

###### Base de datos
- La base de datos no está manejando llaves únicas por lo que pueden existir duplicidades para las 
propiedades y los houmers. Para el caso particular no representa mayor problema, sin embargo
se deberían insertar llaves primarias más ajustadas para que esto no ocurra.
- No se consideraron la inserción de índices, sin embargo los siguientes índices son recomendados:
  - Particionamiento por date para la tabla houmer_position. Esta tabla será intensiva en escritura,
y tendrá muchos datos dado que por cada houmer cada día se insertarán muchas posiciones. 
El particionamiento por fecha en MySql permitiría que la búsqueda e inserción sea más expedita
sin necesidad del sobre costo de un índice. De todos modos el particionamiento actualmente en MySql 
depende del motor. Más información [MySql 8 Partitioning](https://dev.mysql.com/doc/refman/8.0/en/partitioning.html)
  - Para la tabla houmer se debería usar un índice hash en name o alguna llave compuesta.
  - Para la tabla real_state se podría usar un índice Hash compuesto por longitud y latitud,
considerando que las propiedades tienen una única tupla de coordenadas. Para el caso de
departamentos habría que agregar algún campo que especifique en el esquema de la tabla. La tabla
real_state es intensiva en lectura más que en escritura.
  - Para la tabla houmer_position conviene un índice B-Tree por el id del houmer; con un árbol
la búsqueda sería bastante rápida y el costo en espacio del índice no sería tanto dado que se 
consideraría un bigint solamente.
  - Para la tabla houmer_visit_real_state conviene un B-Tree por el id del houmer (para el caso
particular de las consultas del Challenge).

- Habría que hacer un análisis de costo en espacio de las tablas. La tabla más pesada sería
la de houmer_position dado que diariamente se agregarían muchos datos. Un particionamiento
ayudaría con el backup y con la búsqueda. De todos modos la tabla contiene actualmente sólo 3
campos (2 decimales, un bigint y un date) por tanto eso bajaría un poco los costos en espacio.
- Se puede pensar en una base de datos no relacional (como mongoDb) donde se podría utilizar mejor
el uso de nodos y clusters, además evitaría el uso de modelos de tablas un poco más rígidos.
- Faltaría utilizar alguna herramienta de migrations como Alembic para SqlAlchemy [Alembic](https://alembic.sqlalchemy.org/en/latest/)
de este modo el versionamiento de cambios en la base de datos se hace más manejable.

###### Seguridad
- Falta utilizar algún esquema más seguro y actualizado para el uso del token en las transacciones
con la API. Lo ideal es OAUTH 2.0. Podría usarse alguna herramienta como [Cognito de AWS](https://aws.amazon.com/es/cognito/)
o el equivalente [Identity GCP](https://cloud.google.com/identity/).
- Uso de protocolo HTTPS.
- También el WSGI debería aceptar peticiones desde ciertas IP privadas.

###### Arquitectura
Se puede hacer un diseño más acorde con un modelo serverless de la siguiente forma:
- Base de datos en la nube (por ejemplo Aurora DB en AWS) utilizando Amazon RDS Proxy para
un correcto escalamiento y reliability,
- La api se puede integrar utilizando Api Gateway de AWS o ApiGee y ApiGateway de GCP.
- También se puede utilizar Lambda AWS conectado con API Gateway. Para Lambda bastaría
con dockerizar la aplicación y subirla o simplemente subir el código, modificar los routes por
handlers.


