# -*- coding: utf-8 -*-
# ==============================
# Programa: csv_ingestor
# Descripcion: programa que permite leer un csv
# Autor: Mario Silva
# Argumentos de entrada: --file --head --delimiter
#test cambio branch
# ==============================

## Imports
import sys, os, datetime

## Variables globales
ruta_script = os.path.abspath(os.path.dirname(__file__))
ruta_principal = os.path.abspath(os.path.join(ruta_script, os.pardir))
salida=ruta_principal+'\LOGS\{0}_{1}.log'.format(os.getlogin(), datetime.datetime.now().strftime("%Y_%m_%d %H_%M_%S"))

class Registro:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            

# declaracion de etiquetas de parametros
parametros = {"--file": None, "--head": None, "--delimiter": None}        
args = sys.argv[1:]  # Ignoramos el primer argumento, que es el nombre del script


#declaracion de variables
execution_type=""    
nombre_archivo="" 
delimitador=""
file_header=""

    
## Funciones Auxiliares

#funcion menu de ayuda
def mostrar_ayuda():
    mensaje_ayuda = """
    
    Uso de csv_ingestor.py [opciones]
    Opciones:
        --file          Nombre del csv a leer
        --head          Indica si el archivo tiene o no cabecera (S/N)
        --delimiter     Solicita el caracter que se usa como delimitador del archivo (solo puede ser un caracter)
        --help          Muestra este mensaje de ayuda
        *Si no se ingresan parámetros el programa ejecutará el modo interactivo
    """
    print(mensaje_ayuda)

#funcion para escritura de log
def write_log(message):
    f = open(salida,'a+')
    f.write(message)
    f.write('\n')
    f.close()

#funcion lectura automatizada
def read_files(nombre_archivo):
    registros = []    

    try:
        
        with open(nombre_archivo, 'r') as archivo:
            lineas = archivo.readlines()
            
            if lineas:
                
                if file_header == "S":
                    inicio=1
                    nombres_atributos = lineas[0].strip().split(delimitador)
                    
                else:
                    inicio=0
                    nombres_atributos=["columna"+str(i+1) for i in range(len(lineas[0].strip().split(delimitador)))]    
                    archivo.seek(0)

                for linea in lineas[inicio:]:
                    valores = linea.strip().split(delimitador)
                    if len(valores) == len(nombres_atributos):
                
                        args = {nombres_atributos[i]: valores[i] for i in range(len(nombres_atributos))}
                
                        registro = Registro(**args)
                        registros.append(registro)
                    else:
                        write_log(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        write_log("error en linea " + str(linea))
                        write_log("este registro no será cargado")    
            else:
                write_log(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                write_log("Error, el archivo está vacio: [Errno 2] El archivo "+nombre_archivo+" no tiene contenido")
                sys.exit(2)            
    except FileNotFoundError as e:
        write_log(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        write_log("Error, el archivo no existe: " + str(e))
        sys.exit(2)           
    return registros



## MAIN: Cuerpo del programa

#validacion de argumentos para la ejecucion

if '--help' in args:
    mostrar_ayuda()
    sys.exit(0)
    
if len(args)>=1:
    for arg in args:
        key, value = arg.split("=")
        if key in parametros:
            parametros[key] = value                  
if len(sys.argv) == 1:
    execution_type = "I" #ejecucion interactiva
elif len(sys.argv) == 4: 
    par_archivo = str(parametros["--file"])
    punto = par_archivo.rfind('.')
    if punto == -1:
        nombre_archivo=ruta_principal+'\FILES\{0}.{1}'.format(par_archivo, "csv")
    else:
        nombre_archivo=ruta_principal+'\FILES\{0}.{1}'.format(par_archivo[:punto], "csv")    
    delimitador = str(parametros["--delimiter"])
    if len(delimitador)> 1:
        write_log(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        write_log("Error, delimitador no admitido: [Errno 4] el delimitador solo debe contene un caracter")
        sys.exit(4)
    #TO-DO    
    file_header = parametros["--head"]
    if file_header.upper() not in ("S", "N"):
        write_log(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        write_log("Error, Parametro de cabecera incorrecto: [Errno 4] el parametro solo debe ser S o N")
        sys.exit(4)
    execution_type = "A" #ejecucion automatica
else: 
    #print(len(sys.argv))
    write_log(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    write_log("Error, número de parámetros incorrecto: [Errno 4] consulte las opciones de parametros con --help")
    sys.exit(4)

#solicitud de valores en ejecucion automatica
if execution_type == "I":
    print("Bienvenido a la ejecucion interactiva")
    input_archivo = input("   ingrese el nombre del archivo (sin extension): ")
    par_archivo = str(input_archivo)
    punto = par_archivo.rfind('.')
    if punto == -1:
        nombre_archivo=ruta_principal+'\FILES\{0}.{1}'.format(input_archivo, "csv")
    else:
        nombre_archivo=ruta_principal+'\FILES\{0}.{1}'.format(input_archivo[:punto], "csv")    
    delimitador = input("   ingrese el delimitador del archivo: ")
    while len(delimitador)> 1:
        print("Error, delimitador no admitido")
        delimitador = input("   ingrese el delimitador del archivo: ")
        
    file_header = input("   El archivo posee cabecera? S/N: ")
    while file_header.upper() not in ("S", "N"):
        print("Error, por favor solo responda S o N")
        file_header = input("   El archivo posee cabecera? S/N: ")
    registros = read_files(nombre_archivo)  
    
    tipo_lectura=input("   Desea revisar registros? S/N: ")
    while tipo_lectura.upper() not in ("S", "N"):
        print("Error, por favor solo responda S o N")
        tipo_lectura = input("   Desea revisar registros? S/N: ")
    
    
    for i, registro in enumerate(registros, 1):
        write_log(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        write_log("Registro "+ str(i) + ":")
        for attr, value in registro.__dict__.items():
            write_log(str(attr)+": " + str(value))
        write_log("")    
                  
    if tipo_lectura.upper()=="S":
        
        salir="N"
        while salir == "N":
            print("el archivo posee ", len(registros), "registros")
            lectura_reg=input("   ingrese los registros que desea revisar separados por coma o una q si desea salir: ")
            revision=lectura_reg.strip().split(",")
            contiene_numeros_o_q = any(isinstance(elemento, int) or elemento.lower() == "q" for elemento in revision)
            while contiene_numeros_o_q == False:
                print("Error: solo debe ingresar numero o la letra q")
                lectura_reg=input("   ingrese los registros que desea revisar separados por coma o una q si desea salir: ")
                revision=lectura_reg.strip().split(",")
                contiene_numeros_o_q = any(isinstance(elemento, int) or elemento.lower() == "q" for elemento in revision)
            if "q" in lectura_reg.lower():
                sys.exit(0)                
            for i in revision:
                print(i)
                indice = int(i)-1
                elemento = registros[indice]
                
                print("Registro "+ str(i) + ":")
                for attr, value in elemento.__dict__.items():
                    print(str(attr)+": " + str(value))
                print("")          
else: 
    registros = read_files(nombre_archivo)   
    for i, registro in enumerate(registros, 1):
        write_log(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        write_log("Registro "+ str(i) + ":")
        for attr, value in registro.__dict__.items():
            write_log(str(attr)+": " + str(value))
        write_log("")  # Imprimir línea en blanco entre registros         
    
    
    

## Llamada a funcion Main
#if __name__ == "__main__":
#    main()