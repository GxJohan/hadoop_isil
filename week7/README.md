# Semana 7 - Procesamiento Distribuido con MapReduce

Base tecnica validada para la practica de Semana 7.

## Objetivo

Mantener el mismo proyecto `hadoop_isil` de Semana 5-6 y ampliarlo para ejecutar
un trabajo de Hadoop Streaming con Python sobre el dataset:

```text
ai_student_impact_dataset.csv
```

El ejercicio elegido es:

```text
contar estudiantes por Major_Category
```

## Que incluye esta carpeta

- `docker-compose.week7.yml`: stack Hadoop para Semana 7 con imagenes personalizadas que incluyen `python3`.
- `week7/docker/*.Dockerfile`: Dockerfiles para `namenode`, `datanode`, `resourcemanager`, `nodemanager` e `historyserver`.
- `week7/scripts/mapper_major_category.py`: mapper para extraer la columna `Major_Category`.
- `week7/scripts/reducer_count.py`: reducer generico para sumar resultados.

## Idea de trabajo para el curso

Los alumnos no deben clonar otro proyecto si ya tienen `hadoop_isil`.

Flujo recomendado:

1. Entrar a `hadoop_isil`
2. Ejecutar `git pull`
3. Levantar el stack de Semana 7
4. Subir `ai_student_impact_dataset.csv` a HDFS
5. Ejecutar Hadoop Streaming
6. Revisar el resultado en consola y en `http://localhost:9870`

Solo deben clonar el repositorio quienes todavia no tengan la carpeta `hadoop_isil`.
En ese caso tambien deben clonar `docker-hadoop` dentro (aporta `hadoop.env`):

```bash
git clone https://github.com/GxJohan/hadoop_isil.git
cd hadoop_isil
git clone https://github.com/big-data-europe/docker-hadoop.git
```

En Windows usar **PowerShell** o **Git Bash**, no CMD: CMD no entiende las comillas
simples `'...'` de los comandos `sh -lc`.

## Estructura esperada

```text
hadoop_isil/
├── docker-hadoop/
├── ai_student_impact_dataset.csv
├── docker-compose.week7.yml
├── week7/
│   ├── docker/
│   ├── scripts/
│   └── README.md
├── images/
├── README.md
├── comandos-hadoop.txt
├── index.html
├── week7.html
├── week9.html
└── week12.html
```

## Requisito del dataset

El archivo debe estar en la raiz del proyecto:

```text
hadoop_isil/ai_student_impact_dataset.csv
```

## Comandos validados

Mensajes normales que se pueden ignorar:

- `mesg: ttyname failed: Inappropriate ioctl for device`
- Lineas con `INFO`, por ejemplo `INFO sasl.SaslDataTransferClient ...`
- En Mac con chip Apple: `The requested image's platform (linux/amd64) does not match ...` (funciona igual, mas lento)

### 1. Levantar el entorno de Semana 7

Ejecutar desde tu computadora, estando en la carpeta raiz `hadoop_isil`.

Primero apagar el Hadoop de Semana 5-6 (usa los mismos `container_name`; si no estaba
encendido, no pasa nada):

```bash
cd docker-hadoop
docker compose down
cd ..
```

Luego levantar Semana 7:

```bash
docker compose -f docker-compose.week7.yml up --build -d
docker compose -f docker-compose.week7.yml ps
```

Todos los contenedores deben quedar `(healthy)`. La primera vez tarda varios minutos y
necesita internet, porque `--build` instala Python en cada imagen.

### 2. Verificar Python dentro del entorno

Ejecutar desde tu computadora:

```bash
docker exec namenode sh -lc 'python3 --version && python --version'
docker exec nodemanager sh -lc 'python3 --version && python --version'
```

Resultado esperado:

```text
Python 3.5.3
Python 3.5.3
```

## Cargar el dataset a HDFS

Ejecutar desde tu computadora:

```bash
docker exec namenode /opt/hadoop-3.2.1/bin/hdfs dfs -mkdir -p /data
docker exec namenode /opt/hadoop-3.2.1/bin/hdfs dfs -put -f /workshop/ai_student_impact_dataset.csv /data/
docker exec namenode /opt/hadoop-3.2.1/bin/hdfs dfs -ls -h /data
docker exec namenode sh -lc '/opt/hadoop-3.2.1/bin/hdfs dfs -head /data/ai_student_impact_dataset.csv | head -n 5'
```

## Prueba corta del mapper y reducer

Ejecutar desde tu computadora:

```bash
docker exec namenode sh -lc 'head -n 20 /workshop/ai_student_impact_dataset.csv | python3 /workshop/week7/scripts/mapper_major_category.py | sort | python3 /workshop/week7/scripts/reducer_count.py'
```

Resultado esperado:

```text
Arts      ...
Business  ...
Humanities...
Medical   ...
STEM      ...
```

## Ejecutar el trabajo real de Hadoop Streaming

Se lanza desde dentro del contenedor `namenode`. Asi funciona igual en todos los
sistemas: con `docker exec ... sh -lc '...'` desde PowerShell de Windows se pierden las
comillas internas (`"python3 ..."`) y Hadoop falla con `Required argument: -input`.

Desde tu computadora, entrar al contenedor:

```bash
docker exec -it namenode bash
```

Dentro del contenedor `namenode`, borrar la salida anterior y ejecutar el job:

```bash
cd /workshop/week7/scripts
hdfs dfs -rm -r -f /output_major_category
hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -files mapper_major_category.py,reducer_count.py -mapper "python3 mapper_major_category.py" -reducer "python3 reducer_count.py" -input /data/ai_student_impact_dataset.csv -output /output_major_category
exit
```

## Verificar el resultado

Ejecutar desde tu computadora:

```bash
docker exec namenode /opt/hadoop-3.2.1/bin/hdfs dfs -ls -h /output_major_category
docker exec namenode sh -lc '/opt/hadoop-3.2.1/bin/hdfs dfs -cat /output_major_category/part-00000 | head -n 20'
```

Resultado validado:

```text
Arts       5933
Business   12538
Humanities 9994
Medical    6476
STEM       15059
```

## Verificacion visual en el navegador

Abrir:

```text
http://localhost:9870
```

Luego:

1. Buscar `Utilities`
2. Entrar a `Browse the file system`
3. Revisar `/data`
4. Revisar `/output_major_category`

En `/output_major_category` debe aparecer:

```text
part-00000
```

## Hallazgos tecnicos importantes

- El enfoque si es factible con Windows, macOS y Ubuntu si todos usan Docker.
- No conviene depender del Python local del alumno.
- `python3` debe existir al menos en `namenode` y `nodemanager`.
- El dataset `ai_student_impact_dataset.csv` si funciona bien para Streaming.
- El dataset viejo de 200 MB no era buena opcion para esta parte porque tenia registros partidos por varias lineas.
- Los scripts deben ser compatibles con `Python 3.5.3`, por eso no usan `f-strings`.

## Errores comunes

| Problema | Que hacer |
|---|---|
| `env file ... docker-hadoop/hadoop.env not found` | Falta `docker-hadoop`: desde `hadoop_isil` ejecutar `git clone https://github.com/big-data-europe/docker-hadoop.git` |
| `container name "/namenode" is already in use` | Sigue creado el Hadoop de Semana 5-6: `cd docker-hadoop`, `docker compose down`, `cd ..` |
| En Windows fallan los comandos `sh -lc '...'` | Se esta usando CMD: abrir PowerShell o Git Bash |
| `Required argument: -input` o `Missing argument for option: files` | El job no llego completo: ejecutarlo dentro del contenedor (paso 5) y en una sola linea |
| `NameError: name 'Student_ID'` o `python3\r: No such file or directory` | El comando se pego partido (PowerShell muestra `>>`): `Ctrl+C` y pegarlo en una sola linea |
