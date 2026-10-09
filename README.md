# Semana 5 y 6 - Hadoop con Docker

## 👉 Guía paso a paso: https://gxjohan.github.io/hadoop_isil/

Sigue la guía en ese enlace. Tiene los 10 pasos en orden, con capturas, lo que debes ver en cada paso y la solución a los errores comunes. Ese enlace es la versión oficial de la práctica.

**Meta de la práctica:** levantar Hadoop con Docker dentro de esta carpeta (`hadoop_isil`), subir `datos_200mb.csv` a HDFS y ver el archivo en `http://localhost:9870`, en la carpeta `/data`.

## Antes de empezar

- **Windows:** usa la terminal de **Ubuntu (WSL)** para todo. Docker Desktop debe estar abierto y con *WSL integration* activado para Ubuntu.
- **Mac:** usa la app Terminal o la terminal de VS Code.
- Solo se usa **un** archivo: `datos_200mb.csv`. **No viene en el repositorio** (GitHub no acepta archivos de más de 100 MB). Descárgalo de [examplefile.com/code/csv/200-mb-csv](https://examplefile.com/code/csv/200-mb-csv), ponlo en la carpeta `hadoop_isil` y renómbralo a `datos_200mb.csv`.
- El archivo `ai_student_impact_dataset.csv` es para la Semana 7. Hoy no lo uses.

## Resumen de comandos en orden

Esto es solo para repasar. Para trabajar, usa la guía.

```bash
# ===== TERMINAL DE TU PC =====
cd ~
git clone https://github.com/GxJohan/hadoop_isil.git           # paso 2
cd hadoop_isil
code .
git clone https://github.com/big-data-europe/docker-hadoop.git  # paso 3
ls -lh                                                          # paso 4: debe aparecer datos_200mb.csv
cd docker-hadoop                                                # paso 5
docker compose up -d
docker ps
cd ..                                                           # paso 7
docker cp datos_200mb.csv namenode:/tmp/datos_200mb.csv
docker exec -it namenode bash                                   # paso 8

# ===== DENTRO DEL CONTENEDOR namenode =====
hdfs dfsadmin -safemode wait                                    # paso 9
hdfs dfs -mkdir -p /data
hdfs dfs -put -f /tmp/datos_200mb.csv /data/
hdfs dfs -ls -h /data
exit

# ===== NAVEGADOR =====
# http://localhost:9870 -> Utilities -> Browse the file system -> /data   (paso 10)
```

Para apagar Hadoop al terminar, desde la terminal de tu PC:

```bash
cd ~/hadoop_isil/docker-hadoop
docker compose down
```

El archivo no se borra: la próxima vez que levantes Hadoop, seguirá en `/data`.
