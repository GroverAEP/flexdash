import pandas as pd

reporte = {
    1:{"nombre" : "Ana", "edad": 12 , "carrera": "sis"},
    2:{"nombre" : "Luis", "edad": 10, "carrera": "arq"},
    3:{"nombre" : "Alex", "edad": 10, "carrera": "psi"}
}


lista_nombres = []
lista_edades = []
lista_carrera = []

a = ["nombres", "ads"]

for datos in reporte.values():
    # print(datos["nombre"])
    lista_nombres.append(datos["nombre"])
    lista_edades.append(datos["edad"])
    lista_carrera.append(datos["carrera"])

df = pd.DataFrame({
    "Nombre": lista_nombres,
    "Edad": lista_edades,
    "tag" : lista_carrera
})

nombre_archivo = "Archivo de prueba.xlsx"

df.to_excel(nombre_archivo, index=False)



print("Archivo excel creado")


rf = pd.read_excel(nombre_archivo)

rf.fillna("no hya nd", inplace= True)

print(rf.head())

df.to_excel(nombre_archivo)




json_str =df.to_json(orient="records")
print(json_str)