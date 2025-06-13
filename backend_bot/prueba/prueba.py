import os 
def writeFile(correo):
    with open(nombre_archivo,"w") as archivo:
        archivo.write(correo)

def readFile():
    with open(nombre_archivo,"r") as archivo:
        for linea in archivo:
            print(linea.replace(" ","_"))

def removeFile(nombre_archivo):
    if os.path.exists(nombre_archivo):
        os.remove(nombre_archivo)
        print("archivo eliminado ")
    else:
        print("no esta eliminado este archivo")

directorio_actual = os.getcwd()

directorio_padre =os.path.dirname(directorio_actual)

print(directorio_padre)
nombre_archivo= "archivo de prueba"

correo = "Este es un correo para un destinatario X"

writeFile(correo)

print(f"archivo creado {nombre_archivo}, Creado en directorio: ")