import pandas as pd
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Cargar el CSV
file_path = '/Users/marcelomansilla/proyectos/Workspaces/Radiaficion/MANEJO-RUEDAS-RADIOAFICION/src/Listado.csv'
df = pd.read_csv(file_path, delimiter=';')
licencias = df['Señal Distintiva'].astype(str).tolist()

fecha_hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M")



# Variables globales
activos = []
salidos = []

# Funciones
def autocompletar(event):
    entrada = entry_var.get().upper()
    coincidencias = [lic for lic in licencias if lic.startswith(entrada)]
    if coincidencias and entrada in coincidencias:
        entry_var.set(coincidencias[0])
        actualizar_datos(coincidencias[0])
        entry.icursor(tk.END)

def actualizar_datos(licencia):
    datos = df[df['Señal Distintiva'] == licencia]
    if not datos.empty:
        titular_var.set(datos.iloc[0]['Titular de la Licencia'])
        provincia_var.set(datos.iloc[0]['Provincia'])
        localidad_var.set(datos.iloc[0]['Localidad'])

def agregar_a_rueda():
    licencia = entry_var.get().upper()
    if licencia and licencia not in [r[0] for r in activos]:
        hora_ingreso = datetime.now().strftime('%H:%M:%S')
        activos.append([licencia, titular_var.get(), provincia_var.get(), localidad_var.get(), hora_ingreso, ''])
        actualizar_tablas()

def registrar_salida():
    seleccionado = tabla_activos.selection()
    if seleccionado:
        index = int(seleccionado[0])
        activos[index][5] = datetime.now().strftime('%H:%M:%S')
        salidos.append(activos.pop(index))
        actualizar_tablas()

def reingresar():
    seleccionado = tabla_salidos.selection()
    if seleccionado:
        index = int(seleccionado[0])
        usuario = salidos.pop(index)
        usuario[5] = ''  # Borrar hora de salida
        activos.append(usuario)
        actualizar_tablas()

def mover_arriba():
    seleccionado = tabla_activos.selection()
    if seleccionado:
        index = int(seleccionado[0])
        if index > 0:
            activos[index], activos[index - 1] = activos[index - 1], activos[index]
            actualizar_tablas()
            tabla_activos.selection_set(index - 1)

def mover_abajo():
    seleccionado = tabla_activos.selection()
    if seleccionado:
        index = int(seleccionado[0])
        if index < len(activos) - 1:
            activos[index], activos[index + 1] = activos[index + 1], activos[index]
            actualizar_tablas()
            tabla_activos.selection_set(index + 1)

def generar_html():
    with open("/Users/marcelomansilla/proyectos/Workspaces/Radiaficion/MANEJO-RUEDAS-RADIOAFICION/rueda_en_la_cueva.html", "a", encoding="utf-8") as f:
        f.write(f"<h1>RUEDA EN LA CUEVA 146480MHZ {fecha_hora_actual}</h1>")
        f.write("<table border='1'><tr><th>Señal Distintiva</th><th>Titular</th><th>Provincia</th><th>Localidad</th><th>Hora Ingreso</th><th>Hora Salida</th></tr>")
        for row in activos + salidos:
            f.write("<tr>" + "".join(f"<td>{col}</td>" for col in row) + "</tr>")
        f.write("</table><br>")

def actualizar_tablas():
    for widget in tabla_activos.get_children():
        tabla_activos.delete(widget)
    for i, row in enumerate(activos):
        tabla_activos.insert('', 'end', iid=i, values=row, tags=('activo',))
    
    for widget in tabla_salidos.get_children():
        tabla_salidos.delete(widget)
    for i, row in enumerate(salidos):
        tabla_salidos.insert('', 'end', iid=i, values=row, tags=('salido',))

# Crear la ventana
root = tk.Tk()
root.title("Registro de Rueda de Radioaficionados")
root.configure(bg='#2C2F33')

# Variables
entry_var = tk.StringVar()
titular_var = tk.StringVar()
provincia_var = tk.StringVar()
localidad_var = tk.StringVar()

# Entrada y autocompletado
entry = ttk.Entry(root, textvariable=entry_var, width=30, font=("Arial", 14))
entry.pack(pady=5)
entry.bind("<KeyRelease>", autocompletar)

# Datos de la licencia
info_frame = tk.Frame(root, bg='#2C2F33')
info_frame.pack(pady=5)

labels = ["Titular", "Provincia", "Localidad"]
variables = [titular_var, provincia_var, localidad_var]
for i, (label, var) in enumerate(zip(labels, variables)):
    tk.Label(info_frame, text=label + ":", fg='white', bg='#2C2F33', font=("Arial", 12, "bold"))\
        .grid(row=i, column=0, sticky='w', padx=5, pady=2)
    tk.Label(info_frame, textvariable=var, fg='white', bg='#2C2F33', font=("Arial", 12))\
        .grid(row=i, column=1, sticky='w', padx=5, pady=2)

# Botones
btn_frame = tk.Frame(root, bg='#2C2F33')
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Agregar", command=agregar_a_rueda, bg='#7289DA', fg='black', font=("Arial", 12, "bold"))\
    .grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Salir", command=registrar_salida, bg='#E74C3C', fg='black', font=("Arial", 12, "bold"))\
    .grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Reingresar", command=reingresar, bg='#27AE60', fg='black', font=("Arial", 12, "bold"))\
    .grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="↑", command=mover_arriba, bg='#F1C40F', fg='black', font=("Arial", 12, "bold"))\
    .grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="↓", command=mover_abajo, bg='#F1C40F', fg='black', font=("Arial", 12, "bold"))\
    .grid(row=0, column=4, padx=5)
tk.Button(btn_frame, text="HTML", command=generar_html, bg='#F1C40F', fg='black', font=("Arial", 12, "bold"))\
    .grid(row=0, column=5, padx=5)


# Tablas
tabla_frame = tk.Frame(root, bg='#2C2F33')
tabla_frame.pack()

columns = ["Señal Distintiva", "Titular", "Provincia", "Localidad", "Hora Ingreso", "Hora Salida"]

# Tabla de Activos
tk.Label(tabla_frame, text="Activos", fg='white', bg='#2C2F33', font=("Arial", 14, "bold"))\
    .pack()
tabla_activos = ttk.Treeview(tabla_frame, columns=columns, show='headings', selectmode='browse')
tabla_activos.pack()

for col in columns:
    tabla_activos.heading(col, text=col)

tabla_activos.tag_configure('activo', background='#7289DA', foreground='white')

# Tabla de Salidos
tk.Label(tabla_frame, text="Salidos", fg='white', bg='#2C2F33', font=("Arial", 14, "bold"))\
    .pack()
tabla_salidos = ttk.Treeview(tabla_frame, columns=columns, show='headings', selectmode='browse')
tabla_salidos.pack()

for col in columns:
    tabla_salidos.heading(col, text=col)

tabla_salidos.tag_configure('salido', background='#E74C3C', foreground='white')

root.mainloop()
