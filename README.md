# Semana 5 y 6 - Introducción a Hadoop con Docker

Guía práctica básica para estudiantes de ISIL en el curso de Big Data.

Objetivo de esta práctica:
aprender a levantar un entorno simple de Hadoop con Docker, crear un archivo de prueba, subirlo a HDFS y comprobar que todo funciona tanto por consola como desde el navegador.

## Estructura esperada del proyecto

```text
hadoop_isil/
├── docker-hadoop/
├── datos_200mb.csv
├── README.md
├── index.html
└── comandos-hadoop.txt
```

Explicación sencilla:

- `docker-hadoop/` contiene el entorno Hadoop descargado desde GitHub.
- `datos_200mb.csv` es el archivo de prueba pesado.
- `README.md` contiene la guía paso a paso.
- `index.html` contiene la versión visual de la práctica.
- `comandos-hadoop.txt` contiene los comandos resumidos.

## A. Introducción sencilla

Hadoop es una herramienta pensada para almacenar y procesar grandes cantidades de datos.

- Hadoop sirve para almacenar y procesar grandes cantidades de datos.
- HDFS es el sistema de archivos de Hadoop.
- NameNode es quien organiza la información.
- DataNode es donde se guardan los datos.
- Docker permite usar Hadoop sin instalarlo manualmente.

Idea simple:
en lugar de instalar Hadoop archivo por archivo, Docker descarga contenedores ya preparados para que podamos practicar más rápido.

## B. Requisitos previos

Antes de comenzar, cada estudiante debe tener:

- Docker Desktop instalado.
- Visual Studio Code.
- Git instalado.
- Terminal disponible.

Notas por sistema operativo:

- Windows: se recomienda usar la terminal integrada de VS Code, PowerShell o Git Bash.
- Mac: se recomienda usar la terminal integrada de VS Code o la app Terminal.

Consejo importante:
antes de usar los comandos, abre Docker Desktop y espera a que indique que el motor de Docker está corriendo.

## C. Regla importante

> Regla importante:
> Si el comando inicia con `docker`, normalmente se ejecuta desde tu computadora.
> Si el comando inicia con `hdfs dfs`, normalmente se ejecuta dentro del contenedor `namenode`.

## D. Verificar que Docker funciona

### Ejecutar desde la carpeta raiz `hadoop_isil`

```bash
docker --version
docker compose version
docker ps
```

Que deberia aparecer:

- En `docker --version` debe aparecer una version de Docker.
- En `docker compose version` debe aparecer una version de Docker Compose.
- En `docker ps` debe aparecer una tabla.
- Si la tabla sale vacia, no hay problema: solo significa que todavia no hay contenedores en ejecucion.

Si aparece un error como "cannot connect to the Docker daemon":

- Revisa que Docker Desktop este abierto.
- Espera unos segundos.
- Ejecuta otra vez `docker ps`.

## E. Descargar el repositorio de Hadoop con Docker

### Ejecutar desde la carpeta raiz `hadoop_isil`

```bash
git clone https://github.com/big-data-europe/docker-hadoop.git
cd docker-hadoop
```

Que hace cada comando:

- `git clone ...` descarga el repositorio del ejemplo de Hadoop con Docker.
- `cd docker-hadoop` entra a la carpeta del proyecto descargado.

## F. Levantar Hadoop

Debes ejecutar este paso estando dentro de:

```text
hadoop_isil/docker-hadoop
```

### Ejecutar desde la carpeta `docker-hadoop`

```bash
docker compose up -d
```

Explicacion basica:

- Docker descargara imagenes si es la primera vez.
- Luego levantara los contenedores en segundo plano.
- Este paso puede tardar algunos minutos en la primera ejecucion.

## G. Verificar contenedores

### Ejecutar desde tu computadora

Puedes seguir dentro de la carpeta `docker-hadoop` y ejecutar:

```bash
docker ps
```

Deberian aparecer contenedores como:

- `namenode`
- `datanode`
- `resourcemanager`
- `nodemanager`
- `historyserver`

Si alguno tarda en aparecer, espera un poco y vuelve a ejecutar `docker ps`.

## H. Abrir Hadoop en el navegador

### Ejecutar desde tu navegador

Abre estas direcciones:

- `http://localhost:9870`
- `http://localhost:8088`

Explicacion basica:

- `localhost:9870` permite ver el NameNode y explorar HDFS.
- `localhost:8088` permite ver YARN / ResourceManager.

Nota importante:
la comprobacion principal de esta practica es `http://localhost:9870`, porque ahi veremos HDFS.

## I. Primera prueba en HDFS

### Ejecutar desde tu computadora

```bash
docker exec -it namenode bash
```

Despues de este comando, la terminal entra al contenedor `namenode`.

### Ejecutar dentro del contenedor namenode

```bash
echo "hadoop big data hadoop universidad datos datos hdfs" > /tmp/texto.txt
hdfs dfs -mkdir -p /input
hdfs dfs -put -f /tmp/texto.txt /input/
hdfs dfs -ls /input
hdfs dfs -cat /input/texto.txt
```

Que deberias comprobar:

- La carpeta `/input` debe existir en HDFS.
- El archivo `texto.txt` debe aparecer en el listado.
- El comando `cat` debe mostrar el texto guardado.

### Para salir del contenedor

```bash
exit
```

## J. Prueba con archivo pesado

El archivo CSV de prueba fue descargado desde:

`https://examplefile.com/code/csv/200-mb-csv`

Importante:
el nombre real del archivo descargado puede variar. Para esta guia trabajaremos con el nombre:

```text
datos_200mb.csv
```

Lo ideal es que el archivo quede en esta ruta:

```text
hadoop_isil/datos_200mb.csv
```

### Ejecutar desde la carpeta raiz `hadoop_isil` - verificar el nombre real del archivo

Mac / Linux:

```bash
ls -lh
```

Windows PowerShell:

```powershell
dir
```

### Si el archivo tiene otro nombre, renombrarlo

Mac / Linux:

```bash
mv nombre_original.csv datos_200mb.csv
```

Windows PowerShell:

```powershell
ren nombre_original.csv datos_200mb.csv
```

### Opcion A: ejecutar desde la carpeta raiz `hadoop_isil`

```bash
docker cp datos_200mb.csv namenode:/tmp/datos_200mb.csv
```

### Opcion B: ejecutar desde la carpeta `docker-hadoop`

```bash
docker cp ../datos_200mb.csv namenode:/tmp/datos_200mb.csv
```

### Luego ejecutar desde tu computadora

```bash
docker exec -it namenode bash
```

### Ejecutar dentro del contenedor namenode

```bash
hdfs dfs -mkdir -p /data
hdfs dfs -put -f /tmp/datos_200mb.csv /data/
hdfs dfs -ls -h /data
hdfs dfs -head /data/datos_200mb.csv
```

Resultado esperado:

- El archivo debe aparecer dentro de `/data`.
- `hdfs dfs -ls -h /data` debe mostrar el nombre del archivo y su tamano.
- `hdfs dfs -head /data/datos_200mb.csv` debe mostrar las primeras lineas del archivo.

### Para salir del contenedor

```bash
exit
```

## K. Verificacion visual en localhost:9870

### Abrir en el navegador

`http://localhost:9870`

### Buscar en la interfaz

`Utilities -> Browse the file system`

### Revisar la ruta

```text
/input
```

Para ver:

```text
texto.txt
```

### Revisar tambien la ruta

```text
/data
```

Para ver:

```text
datos_200mb.csv
```

Si no aparece en el navegador, verificar por consola dentro del contenedor:

```bash
hdfs dfs -ls /input
hdfs dfs -ls -h /data
```

## L. Apagar Hadoop

### Primero salir del contenedor si estas dentro

```bash
exit
```

### Luego entrar a la carpeta `docker-hadoop` si no estas ahi

```bash
cd docker-hadoop
```

### Finalmente ejecutar desde tu computadora

```bash
docker compose down
```

Explicacion:

- Este comando apaga y elimina los contenedores de la practica.
- Los datos temporales de la sesion pueden desaparecer si no estan montados en volumenes.

## M. Problemas comunes

| Problema | Solucion sencilla |
| --- | --- |
| Docker no abre. | Cierra y vuelve a abrir Docker Desktop. Espera hasta que indique que esta funcionando. |
| Puerto 9870 no carga. | Revisa `docker ps`, espera un poco mas y confirma que el contenedor `namenode` esta arriba. |
| `docker compose` no existe. | Actualiza Docker Desktop. En algunos equipos antiguos puede funcionar `docker-compose`, pero en esta guia usaremos `docker compose`. |
| El contenedor `namenode` no aparece. | Asegurate de estar dentro de la carpeta `docker-hadoop` y vuelve a ejecutar `docker compose up -d`. |
| El archivo no se ve en HDFS. | Comprueba con `hdfs dfs -ls /input` o `hdfs dfs -ls -h /data` y luego actualiza el navegador en `localhost:9870`. |
| En Windows el comando no funciona por estar en otra carpeta. | Usa `cd` para entrar a la carpeta correcta. Puedes confirmar con `dir` en PowerShell o `ls` en Git Bash. |
| Estoy dentro del contenedor y `docker ps` no funciona. | Sal con `exit` y ejecuta `docker ps` desde la computadora. |
| Estoy dentro de `docker-hadoop` y no encuentra `datos_200mb.csv`. | Usa `../datos_200mb.csv` o vuelve a la carpeta raiz `hadoop_isil`. |
| El archivo descargado no se llama `datos_200mb.csv`. | Verifica el nombre con `dir` o `ls -lh` y luego renombralo. |
| `localhost:9870` abre, pero no veo el archivo. | Confirma primero que el archivo si se subio a HDFS con `hdfs dfs -ls /input` o `hdfs dfs -ls -h /data`. |

## Cierre

Idea principal de la practica:
Hadoop se trabaja principalmente por comandos, pero `localhost:9870` permite comprobar visualmente que HDFS esta funcionando.
