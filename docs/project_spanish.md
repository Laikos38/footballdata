# Breve explicación del proyecto

## Elección de tecnologías

Django REST Framework es básicamente el default a la hora de implementar una API en Python.

PostgreSQL es mi motor de bd favorito a la hora de conectar con Django, debido a su velocidad, soporte para JSONb y psql.

## Proyecto
El proyecto extrae y parsea los datos de football-data.org en una base de datos local, y luego los hace disponibles a través de una API REST.

## ¿Por qué Celery para importar datos?

Siempre que se trate de tareas como scrapping, consumir otras APIs con throttling alto o tareas de OSINT, se debería usar algún tipo de control de tareas en segundo plano en cola.

En este caso, la tarea se encuentra en el proceso de importación de la data de Football-data.org. Si este proceso se ejecutara sincrónicamente, la request demoraría entre 3 y 10 segundos aproximadamente, lo cual es un mala práctica.

¿Por qué no usar un throttle en el endpoint? 

Nada evita que se consulte el endpoint con diferentes sesiones o un proxy, ejecutando el proceso numerosas veces y provocando que las requests realizadas a football-data respondan con 429 To many requests.

Por lo tanto la decisión fue integrar Celery con Redis como backend para ejecutar este proceso en segundo plano y evitar ejecuciones concurrentes de la tarea.