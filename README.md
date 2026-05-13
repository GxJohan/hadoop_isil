# Semana 5 y 6 - Hadoop con Docker

Guia practica para trabajar Hadoop con Docker desde Visual Studio Code usando una carpeta base llamada `hadoop_isil`.

Objetivo de esta practica:
preparar el entorno, abrir el proyecto en Visual Studio Code, levantar Hadoop con Docker, cargar `datos_200mb.csv` a HDFS y comprobar el resultado en `http://localhost:9870`.

## Estructura esperada del proyecto

```text
hadoop_isil/
├── docker-hadoop/
├── datos_200mb.csv
├── README.md
├── index.html
└── comandos-hadoop.txt
```

Explicacion corta:

- `docker-hadoop/` contiene el entorno Hadoop descargado desde GitHub.
- `datos_200mb.csv` es el archivo pesado de prueba.
- `README.md` contiene la guia paso a paso.
- `index.html` contiene la version visual de la practica.
- `comandos-hadoop.txt` contiene el resumen rapido de comandos.

## A. Conceptos base

- Hadoop sirve para almacenar y procesar grandes cantidades de datos.
- HDFS es el sistema de archivos de Hadoop.
- NameNode organiza la informacion.
- DataNode guarda los datos.
- Docker permite usar Hadoop sin instalarlo manualmente.

## B. Instalacion previa

Antes de comenzar, instala estas herramientas:

- Docker Desktop
- Visual Studio Code
- Git
- Terminal disponible

### Windows

1. Instala Visual Studio Code desde [code.visualstudio.com](https://code.visualstudio.com/).
2. Instala Git desde [git-scm.com/download/win](https://git-scm.com/download/win).
3. Usa la terminal integrada de VS Code, PowerShell o Git Bash.
4. Abre Docker Desktop antes de iniciar la practica.

### Mac

1. Instala Visual Studio Code desde [code.visualstudio.com](https://code.visualstudio.com/).
2. Instala Git desde [git-scm.com/download/mac](https://git-scm.com/download/mac) o verifica si ya existe con `git --version`.
3. Usa la terminal integrada de VS Code o la app Terminal.
4. Abre Docker Desktop y espera a que el motor este activo.

## C. Regla importante

> Si el comando inicia con `docker`, normalmente se ejecuta desde tu computadora.
>
> Si el comando inicia con `hdfs dfs`, normalmente se ejecuta dentro del contenedor `namenode`.

## D. Repositorio base y Visual Studio Code

Repositorio base del curso:
[https://github.com/GxJohan/hadoop_isil](https://github.com/GxJohan/hadoop_isil)

### Ejecutar desde tu computadora

```bash
git clone https://github.com/GxJohan/hadoop_isil.git
cd hadoop_isil
code .
```

Si `code .` no funciona:

- abre Visual Studio Code manualmente
- usa `File -> Open Folder`
- selecciona la carpeta `hadoop_isil`

## E. Verificar que Docker funciona

### Ejecutar desde la carpeta raiz `hadoop_isil`

```bash
docker --version
docker compose version
docker ps
```

Que deberia aparecer:

- una version de Docker
- una version de Docker Compose
- una tabla de contenedores

Si la tabla sale vacia, no hay problema. Solo significa que todavia no hay contenedores en ejecucion.

## F. Descargar el entorno Hadoop dentro de la carpeta base

### Ejecutar desde la carpeta raiz `hadoop_isil`

```bash
git clone https://github.com/big-data-europe/docker-hadoop.git
cd docker-hadoop
```

## G. Levantar Hadoop

Este paso debe ejecutarse estando dentro de:

```text
hadoop_isil/docker-hadoop
```

### Ejecutar desde la carpeta `docker-hadoop`

```bash
docker compose up -d
docker ps
```

Que debes comprobar:

- deben aparecer contenedores como `namenode`, `datanode`, `resourcemanager`, `nodemanager` e `historyserver`
- si tardan en aparecer, espera unos segundos y vuelve a ejecutar `docker ps`

## H. Abrir Hadoop en el navegador

Abre estas direcciones:

- `http://localhost:9870`
- `http://localhost:8088`

Explicacion corta:

- `localhost:9870` muestra el NameNode y permite explorar HDFS
- `localhost:8088` muestra YARN / ResourceManager

La comprobacion principal de esta practica se hace en `http://localhost:9870`.

## I. Prueba con archivo pesado

El archivo fue descargado desde:
[https://examplefile.com/code/csv/200-mb-csv](https://examplefile.com/code/csv/200-mb-csv)

Importante:
el nombre real del archivo descargado puede variar. Para esta guia se usara el nombre:

```text
datos_200mb.csv
```

La ubicacion recomendada es:

```text
hadoop_isil/datos_200mb.csv
```

### Paso 1 - Verificar el nombre real del archivo

#### Mac / Linux

```bash
ls -lh
```

#### Windows PowerShell

```powershell
dir
```

### Paso 2 - Renombrar el archivo si tiene otro nombre

#### Mac / Linux

```bash
mv nombre_original.csv datos_200mb.csv
```

#### Windows PowerShell

```powershell
ren nombre_original.csv datos_200mb.csv
```

### Paso 3A - Copiar el CSV al contenedor desde `hadoop_isil`

### Ejecutar desde tu computadora

```bash
docker cp datos_200mb.csv namenode:/tmp/datos_200mb.csv
docker exec -it namenode bash
```

### Paso 3B - Copiar el CSV al contenedor desde `docker-hadoop`

### Ejecutar desde tu computadora

```bash
docker cp ../datos_200mb.csv namenode:/tmp/datos_200mb.csv
docker exec -it namenode bash
```

Despues de `docker exec -it namenode bash`, tu terminal entra al contenedor `namenode`.

### Paso 4 - Subir el archivo a HDFS

### Ejecutar dentro del contenedor namenode

```bash
hdfs dfs -mkdir -p /data
hdfs dfs -put -f /tmp/datos_200mb.csv /data/
hdfs dfs -ls -h /data
hdfs dfs -head /data/datos_200mb.csv
```

Resultado esperado:

- `hdfs dfs -ls -h /data` debe mostrar `datos_200mb.csv`
- `hdfs dfs -head /data/datos_200mb.csv` debe mostrar las primeras lineas del archivo

### Paso 5 - Salir del contenedor

### Ejecutar dentro del contenedor namenode

```bash
exit
```

## J. Verificacion visual en localhost:9870

1. Abrir `http://localhost:9870`
2. Buscar `Utilities -> Browse the file system`
3. Escribir `/data`
4. Verificar que aparezca `datos_200mb.csv`

Si no aparece, comprobar primero por consola:

### Ejecutar dentro del contenedor namenode

```bash
hdfs dfs -ls -h /data
```

## K. Apagar Hadoop

Si todavia estas dentro del contenedor:

### Ejecutar dentro del contenedor namenode

```bash
exit
```

Luego vuelve a `docker-hadoop` si hace falta.

### Ejecutar desde tu computadora - carpeta `docker-hadoop`

```bash
docker compose down
```

## L. Problemas comunes

| Problema | Solucion sencilla |
| --- | --- |
| Docker no abre. | Abre Docker Desktop y espera hasta que este operativo. |
| `docker compose` no existe. | Actualiza Docker Desktop. En algunos equipos antiguos puede existir `docker-compose`. |
| El contenedor `namenode` no aparece. | Revisa que estes dentro de `docker-hadoop` y vuelve a ejecutar `docker compose up -d`. |
| Estoy dentro del contenedor y `docker ps` no funciona. | Sal con `exit` y ejecuta `docker ps` desde tu computadora. |
| Estoy en `docker-hadoop` y no encuentra `datos_200mb.csv`. | Usa `../datos_200mb.csv` o vuelve a la carpeta raiz `hadoop_isil`. |
| El archivo descargado no se llama `datos_200mb.csv`. | Verifica el nombre con `dir` o `ls -lh` y luego renombralo. |
| `localhost:9870` abre, pero no veo el archivo. | Confirma primero que el archivo si se subio con `hdfs dfs -ls -h /data`. |

## Cierre

Idea principal de la practica:
Hadoop se trabaja principalmente por comandos, pero `localhost:9870` permite comprobar visualmente que HDFS esta funcionando y que el archivo pesado ya llego a la ruta `/data`.
