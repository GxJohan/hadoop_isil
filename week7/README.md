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

## Estructura esperada

```text
hadoop_isil/
├── docker-hadoop/
├── ai_student_impact_dataset.csv
├── docker-compose.week7.yml
└── week7/
    ├── docker/
    ├── scripts/
    └── README.md
```

## Requisito del dataset

El archivo debe estar en la raiz del proyecto:

```text
hadoop_isil/ai_student_impact_dataset.csv
```

## Comandos validados

### 1. Levantar el entorno de Semana 7

Ejecutar desde tu computadora, estando en la carpeta raiz `hadoop_isil`:

```bash
docker compose -f docker-compose.week7.yml up --build -d
docker compose -f docker-compose.week7.yml ps
```

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

Primero, borrar una salida anterior si ya existe:

```bash
docker exec namenode /opt/hadoop-3.2.1/bin/hdfs dfs -rm -r -f /output_major_category
```

Luego ejecutar el job:

```bash
docker exec namenode sh -lc '/opt/hadoop-3.2.1/bin/hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -files /workshop/week7/scripts/mapper_major_category.py,/workshop/week7/scripts/reducer_count.py -mapper "python3 mapper_major_category.py" -reducer "python3 reducer_count.py" -input /data/ai_student_impact_dataset.csv -output /output_major_category'
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
