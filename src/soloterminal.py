import pandas as pd
from datetime import datetime

# Cargar el CSV
file_path = '/Users/marcelomansilla/proyectos/Workspaces/Radiaficion/ruedas/RUEDAS-MANEJA/Listado.csv'
df = pd.read_csv(file_path, delimiter=';')
licencias = df['Señal Distintiva'].astype(str).tolist()

# Variables globales
activos = []
salidos = []

def buscar_licencia(licencia):
    datos = df[df['Señal Distintiva'] == licencia]
    if not datos.empty:
        return {
            "Titular": datos.iloc[0]['Titular de la Licencia'],
            "Provincia": datos.iloc[0]['Provincia'],
            "Localidad": datos.iloc[0]['Localidad']
        }
    return None

def agregar_a_rueda():
    licencia = input("Ingrese la señal distintiva: ").upper()
    datos = buscar_licencia(licencia)
    if datos and licencia not in [r[0] for r in activos]:
        hora_ingreso = datetime.now().strftime('%H:%M:%S')
        activos.append([licencia, datos['Titular'], datos['Provincia'], datos['Localidad'], hora_ingreso, ''])
        print(f"{licencia} agregado a la rueda.")
    else:
        print("Licencia no encontrada o ya activa.")

def registrar_salida():
    licencia = input("Ingrese la señal distintiva a salir: ").upper()
    for i, usuario in enumerate(activos):
        if usuario[0] == licencia:
            usuario[5] = datetime.now().strftime('%H:%M:%S')
            salidos.append(usuario)
            activos.pop(i)
            print(f"{licencia} registrado como salido.")
            return
    print("Licencia no encontrada en activos.")

def mostrar_listas():
    print("\nActivos:")
    for usuario in activos:
        print(usuario)
    print("\nSalidos:")
    for usuario in salidos:
        print(usuario)

def generar_html():
    fecha_hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    with open("/Users/marcelomansilla/proyectos/Workspaces/Radiaficion/ruedas/RUEDAS-MANEJA/rueda_en_la_cueva.html", "a", encoding="utf-8") as f:
        f.write(f"<h1>RUEDA EN LA CUEVA 146480MHZ {fecha_hora_actual}</h1>")
        f.write("<table border='1'><tr><th>Señal Distintiva</th><th>Titular</th><th>Provincia</th><th>Localidad</th><th>Hora Ingreso</th><th>Hora Salida</th></tr>")
        for row in activos + salidos:
            f.write("<tr>" + "".join(f"<td>{col}</td>" for col in row) + "</tr>")
        f.write("</table><br>")
    print("HTML generado.")

def menu():
    while True:
        print("\n1. Agregar a la rueda")
        print("2. Registrar salida")
        print("3. Mostrar listas")
        print("4. Generar HTML")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            agregar_a_rueda()
        elif opcion == '2':
            registrar_salida()
        elif opcion == '3':
            mostrar_listas()
        elif opcion == '4':
            generar_html()
        elif opcion == '5':
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
