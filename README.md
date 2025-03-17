# GIT
## BRANCHES
Template: `<type>/<issue>/<description>`

## COMMITS
Template: `<type>(scope): <description>`

### TYPES:
- build: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
- ci: Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)
- docs: Documentation only changes
- feat: A new feature
- fix: A bug fix
- perf: A code change that improves performance
- refactor: A code change that neither fixes a bug nor adds a feature
- style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- test: Adding missing tests or correcting existing tests


# Preguntas prueba tecnica
Imagina que en esta aplicación adicionalmente se quiere tener métricas de
lectura basadas en eventos y está siendo utilizada por un millón de usuarios
simultáneos.

1. ¿Cómo gestionarías esta cantidad de datos a nivel técnico?

En experiencias previas, he trabajado con bases de datos NoSQL como MongoDB. Para casos concretos, este tipo de base de datos ofrece un buen rendimiento. En el caso de MongoDB, si trabajas con Atlas, también tienes la oportunidad de utilizar filtros avanzados que siguen el mismo esquema que Elasticsearch, ya que está construido sobre el mismo motor.

Como tecnología que puede aportar mucho valor en este tipo de escenarios, me gustaría mencionar ClickHouse. Es una base de datos tabular con un rendimiento excepcional. He realizado pruebas sobre tablas con más de 2.6 billones de filas y, al aplicar filtros, he obtenido resultados impresionantes en tan solo unos milisegundos.
https://clickhouse.com/


2. ¿Qué tipo de base de datos utilizarías para almacenar las métricas de
lectura de los usuarios? ¿Por qué?

En el caso de MongoDB, se utiliza BSON. Sin embargo, volviendo a la tecnología que mencioné anteriormente, los datos se almacenan en formato Parquet.
Personalmente, cada vez me convence menos el almacenamiento de información en JSON o BSON, ya que considero que no es una forma óptima de almacenar los datos.


3. ¿Has trabajado con alguna base de datos o infraestructura que soporte un
volumen alto de usuarios y datos? Si es así, cuéntanos tu experiencia y qué
tecnologías utilizaste.

He tenido la oportunidad de trabajar con una base de datos que almacenaba información de más de 4.5 millones de usuarios, incluyendo todos los datos de sus interacciones.

En nuestro caso, trabajábamos con dos bases de datos. Una de ellas estaba construida en MongoDB y en ella almacenábamos una gran cantidad de información sobre los usuarios, como sus intereses dentro de nuestra plataforma.
También guardábamos datos de ciertos escenarios para realizar búsquedas personalizadas muy específicas. Un ejemplo de esto era nuestro buscador de ciudades, que tenía en cuenta la ubicación del usuario, las ciudades más cercanas y sus principales intereses. Para ello, utilizábamos un esquema en MongoDB con toda la información de las ciudades. Luego, pasábamos la geolocalización del usuario y, además, las ubicaciones de los conciertos a los que había asistido. Con toda esta información, realizábamos búsquedas a través de MongoDB Atlas utilizando el motor de Lucene.

https://lucene.apache.org/core/
https://parquet.apache.org/
