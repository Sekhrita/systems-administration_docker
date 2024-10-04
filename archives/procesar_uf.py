import os
import pytz
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

#INSTRUCCIÓN: Configuración de la zona horaria de Chile
CHILE_TZ = pytz.timezone('America/Santiago')

# VARIABLE: Establecer las rutas de los archivos
INPUT_FILE = 'input/entrada.csv'
OUTPUT_FOLDER = 'output/'
LOG_FILE = os.path.join(OUTPUT_FOLDER, 'error.log')

# VALIDACIÓN: Asegurar la existencia de la carpeta de salida
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# FUNCIÓN: Obtener hora actual en Chile
def obtener_hora_actual():
    return datetime.now(CHILE_TZ)

# FUNCIÓN: Genera el archivo '.log' en caso de error
def log_error(error_message):
    # VARIABLE: Registrar la hora de aparición del error en el formato indicado (yy-mm-dd HH_mi_ss)
    timestamp = obtener_hora_actual().strftime("%Y-%m-%d %H:%M:%S")

    # INTRUCCIÓN: Creación y escritura del archivo '.log' con el mensaje del error
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {error_message}\n")

# FUNCIÓN: Revisar el formato del archivo '.csv' de entrada
def validar_csv(data):
    # VARIABLE: Arreglo con las columnas solicitadas
    required_columns = ['dia', 'valor_uf']

    # VALIDACIÓN: Se asegura de que el archivo '.csv' presente el formato necesario
    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"El archivo CSV no contiene las columnas necesarias: {required_columns}")

# FUNCIÓN: Generar el gráfico en base al archivo de entrada
def generar_grafico(data, output_file):
    plt.figure(figsize=(10, 8)) # Tamaño del gráfico
    plt.plot(data['dia'], data['valor_uf'], color='purple', marker='o', linestyle='-') # Características
    plt.xlabel('Fecha')
    plt.ylabel('Valor UF')
    plt.xticks(rotation=75) # Pequeña inclinación en las fechas para mejor legibilidad
    plt.title('Variación del valor UF en el tiempo')
    plt.savefig(output_file)
    plt.close()

# FUNCIÓN: Leer y dar formato al archivo de entrada. Crear el gráfico en base a los datos
def procesar_csv(input_file, output_folder):
    # INSTRUCCIÓN: Abrir y leer el archivo '.csv'
    data = pd.read_csv(input_file)

    # INSTRUCCIÓN: Comprobar formato
    validar_csv(data)

    # INSTRUCCIÓN: Convesión de la columna 'dia' a formato de fecha
    data['dia'] = pd.to_datetime(data['dia'])

    # VARIABLE: Guardar el momento de creación del gráfico (yy-mm-dd HH-mi-ss)
    timestamp = obtener_hora_actual().strftime("%Y-%m-%d_%H-%M-%S")

    # INSTRUCCIÓN: Generar y establecer el nombre del gráfico de salida.
    output_file = os.path.join(output_folder, f'salida_{timestamp}.jpg')
    generar_grafico(data, output_file)

    # FLAG: Gráfico generado con éxito
    print(f"Gráfico guardado en: {output_file}")

    # INSTRUCCIÓN: Almacenar los datos procesados utilizados para la creación del gráfico
    store_file = os.path.join(output_folder, 'entrada.csv.store')
    data.to_csv(store_file, mode='a', header=not os.path.exists(store_file), index=False)

# FUNCIÓN 'MAIN': Inicia el proceso de lectura y generación del gráfico junto a validaciones
def procesar_uf():
    # INSTRUCCIÓN: Controla el flujo del código y el manejo de errores
    try:
	# VALIDACIÓN: Si existe el archivo '.csv' de entrada, se continúa con el programa
        if not os.path.exists(INPUT_FILE):
            raise FileNotFoundError(f"El archivo {INPUT_FILE} no existe.")
        procesar_csv(INPUT_FILE, OUTPUT_FOLDER)

    except FileNotFoundError as fnf_error:
	# VALIDACIÓN: No se encontró el archivo de entrada. Llamar la creación de 'error.log'
        log_error(fnf_error)

	# FLAG: El código llego hasta el "error de archivo de entrada no encontrado"
        print("Error: Archivo no encontrado. Revisa el archivo error.log.")

    except pd.errors.EmptyDataError:
	# VALIDACIÓN: El archivo de entrada se encuentra vacío. Llamar la creación de 'error.log'
        log_error("Error: El archivo CSV está vacío.")

	# FLAG: El código llego hasta el "error de archivo de entrada vacío"
        print("Error: Archivo CSV vacío. Revisa el archivo error.log.")

    except ValueError as ve:
	# VALIDACIÓN: El archivo de entrada no tiene el formato deseado. Llamar la creación de 'error.log'
        log_error(ve)

	# FLAG: El código llego hasta el "error de formato o de datos en el archivo de entrada"
        print("Error: Problema con los datos. Revisa el archivo error.log.")

    except Exception as e:
	# VALIDACIÓN: Se encontró un error no previsto. Llamar la creación de 'error.log'
        log_error(f"Error inesperado: {str(e)}")

	# FLAG: El código llego hasta el "error imprevisto"
        print("Error inesperado. Revisa el archivo error.log.")

# MAIN
if __name__ == "__main__":
    # INSTRUCCIÓN: Llamar a función main e iniciar el flujo del programa
    procesar_uf()
