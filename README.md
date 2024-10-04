# Administración de sistemas - Tarea 2: Archivos Docker

- Estudiante: Felipe Carreño Aravena

- Profesor: Francisco Aravena Oñate

- Fecha: Octubre 4, 2024


## Descripción del proyecto
Este proyecto es una maqueta diseñada para aprender y practicar Docker, usando un script de Python que procesa datos de la Unidad de Fomento (UF). El objetivo es explorar conceptos clave de Docker, como la creación de imágenes, la ejecución de contenedores y el uso de volúmenes para compartir archivos entre el host y el contenedor.

El script lee un archivo de entrada (entrada.csv), genera un gráfico de la UF y guarda los resultados en una carpeta compartida. Docker permite ejecutar el script en cualquier máquina sin necesidad de configurar dependencias manualmente.

Funcionalidades principales:
--> Contenedorización: El proyecto garantiza un entorno consistente con Docker.
--> Procesamiento de datos: Lee datos de un archivo CSV proporcionado por el host.
--> Generación de gráficos: Usa matplotlib y panda para mostrar la variación de la UF en el tiempo con un gráfico.
--> Almacenamiento: Los gráficos se guardan en la carpeta output compartida entre el host y el contenedor.
--> Registro de datos: Los datos se agregan a un archivo de registro (entrada.csv.store).
--> Manejo de errores: Genera un archivo error.log si faltan archivos o se produce un error.

## Instalación de Docker
### Preparación
1.- Primero se debe asegurar que los paquetes del sistemas se encuentren actualizados:
```bash
sudo apt update && sudo apt upgrade -y
```

2.- Luego se deben instalar las dependencias necesarias para el funcionamiento de Docker:
```bash
sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release software-properties-common -y
```

3.- También se debe agregar la clave GPG para permitir las descargas del repositorio de Docker:
```bash
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

4.- Se prosigue con la adición del repositorio oficial de Docker a APT:
```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

5.- Finalmente, se vuelven a actualizar los repositorios:
```bash
sudo apt update
```

### Instalación
Se puede realizar la instalación de Docker (Docker Community Edition) con el siguiente comando:
```bash
sudo apt install docker-ce
```

### Integridad de la instalación
1.- Con la opción '-versión', en una instalación fructífera, nos permitirá ver la versión del programa:
```bash
sudo docker --version
```

2.1.- Se puede iniciar el servicio de Docker:
```bash
sudo systemctl start docker
```

2.2.- Se puede habilitar para que se inicie automáticamente:
```bash
sudo systemctl enable docker
```

2.3.- Finalmente, se puede revisar su estado para asegurar un correcto funcionamiento (debería de aparecer running):
```bash
sudo systemctl status docker
```

### Permisos al usuario para utilizar Docker (opcional)
Con el siguiente comando se modifican los grupos para permitirle al usuario el utilizar Docker sin sudo:
```bash
sudo usermod -aG docker $USER
```

## Creación del entorno
### Opción 1: Clonación del repositorio
Para correr el proyecto se puede clonar el repositorio de git para obtener automáticamente el entorno de trabajo. Por ejemplo, se puede clonar con HTTPS:
```bash
git clone https://github.com/Sekhrita/systems-administration_docker.git
```

### Opción 2: Creación manual
También, se puede crear el entorno de trabajo de manera manual. Para esto es necesario crear dos carpetas: una de "input" y otra de "output"; es requerido que lleven esos mismos nombres, ya que el script de Python está hecho y "hardcodeado" para detectar esos directorios. De igual manera, es necesario que el archivo de entrada tenga un nombre y formato en específico, por ejemplo:
--> Archivo: entrada.csv
```
dia,valor_uf
2024-09-01,28050.3
2024-09-02,28075.9
2024-09-03,28100.5
2024-09-04,28120.1
```

#### Estructura de archivos esperada
En el siguiente esquema, los scripts de docker y python se puede observar y descargar desde el presente repositorio de git:
```
/workdir
├── dockerfile
├── procesar_uf.py
├── input
│   └── entrada.csv
└── output
```

## Explicación de los scripts
### Dockerfile
Breve explicación del archivo Docker:
1.- FROM: Establece la imagen base que usará el contenedor. La imagen base es un sistema operativo mínimo que incluye lo necesario para ejecutar el programa que se va a correr. En el caso del proyecto, se utiliza 'python:3.9-slim' el cual es una imagen ligera de Python en la versión 3.9, lo que reduce el tamaño del contenedor en comparación con versiones completas de Python.

2.- WORKDIR: Permite definir el directorio de trabajo dentro del contenedor, es decir, la carpeta en la que se estará trabajando y donde se ejecutarán los comandos posteriores. Para el proyecto se utilizará el directorio '/task-docker', donde se copiarán los archivos y donde se ejecutará el script.

3.- COPY: Esto copia archivos o directorios desde el sistema del host hacia el sistema de archivos del contenedor. En el proyecto se utiliza para que el archivo 'procesar_uf.py' se copie desde el host al directorio de trabajo '/task-docker' del contenedor.

4.- RUN: Instrucción que ejecuta comandos en el proceso de creación del contenedor. Estos comandos son parte de la construcción de la imagen, no se ejecutan cada vez que se corre el contenedor, sino solo cuando se está creando. Por lo que, viene bien para definir e instalar las dependencias que el script necesita (matplotlib, pandas y pytz) utilizando pip, el gestor de paquetes de Python.

5.- CMD: Finalmente, 'CMD' define el comando que se ejecutará cuando el contenedor se inicie. A diferencia de RUN, que es para construir la imagen, CMD es lo que se ejecuta cada vez que el contenedor se corre. Para el proyecto se necesita que el contenedor corra el comando python 'procesar_uf.py' cada vez que se ejecute, esto asegurará que el script de un resultado.

### Script de python
Dada la extensión del script, es preferible que para más información se revise manualmente el código; esté se encuentra altamente comentado para facilitar su entendimiento. Como apreciación general, he de decir que falta integrar algunos casos de error, como por ejemplo: mandar error cuando los datos de 'uf' presenten nulos, actualmente solo los ignora; mismo caso si presentan caracteres distintos a números. Los casos de error que si se verifican son: si no existe archivo de entrada, si el archivo de entrada se encuentra vacío, si el archivo de entrada no tiene el formato deseado y, para terminar, que la fecha de 'dia', dentro del archivo, tenga un formato distinto a 'YY-mm-dd'.


## Inicializar contenedor (docker):
### Crear el contenedor
Una vez realizadas las instalaciones pertinentes, en conjunto con la creación minuciosa del entorno de trabajo, se puede comenzar con la creación del contenedor con 'build', el cual construye una imagen docker a partir de un 'dockerfile':
```bash
docker build -t procesador-if:1.0 .
```
La opción '-t' permite añadirle un nombre a la imagen; lo que se encuentra luego de los ":" es la versión de la imagen: el "." indica que en el directorio donde se tire este comando, se encuentra el 'dockerfile' que se utilizara en la creación del contenedor.

### Comprobar la imagen
Este comando permite verificar que se haya creado la imagen correctamente y sus propiedades. Se utilizará para obtener la id de la imagen:
```bash
docker images
```

### Correr el contenedor
Ahora se puede ejecutar un contenedor basado en una imagen específica. En este caso se utilizará la 'id_image' de la imagen que se acaba de crear:
```bash
docker run -v $(pwd)/input:/task-docker/input -v $(pwd)/output:/task-docker/output <IMAGE_ID>
```
La opción '-v' con '$(pwd)/input:/task-docker/input' y '$(pwd)/output:/task-docker/output' permite montar carpetas locales (input y output) en el contenedor, permitiendo el intercambio de archivos e información. A esto se le llama trabajar con volúmenes, los cuales son un puente entre el host y el contenedor.
