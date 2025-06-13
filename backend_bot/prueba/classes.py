class Auto:


    def __init__(self,nombre,matricula):
        self._nombre = nombre,
        self.__matricula = matricula
    
    def __str__(self):
        return f"Auto placa: {self.__matricula}"


    def _mostrarMatricula(self):
        return self.__matricula 



import pandas as pd
import random as rd

list_name= []
list_matricula=[]



caracteres = "ABCDFG"

for i in range(1,10):


    lista_cadena = list(caracteres)
    muestra = rd.sample(caracteres,3)
    print(muestra)

    new_code = ''.join(muestra)
    print(new_code)




    nuevo_auto = Auto(f"Auto: {i}",f"#{new_code}S3")
    print(nuevo_auto)
    # print(nuevo_auto.mostrarMatricula())

    

    list_name.append(nuevo_auto._nombre)
    list_matricula.append(nuevo_auto._mostrarMatricula())

    df =  pd.DataFrame({
            "Nombre_autos": list_name, 
            "matricula": list_matricula
        })


print(df.head())

df.to_excel("Lista de matricula.xlsx", index=False)





