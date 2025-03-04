import os
import subprocess

# Configuración
REPO_PATH = "/ruta/del/repositorio"  # Reemplaza con la ruta local del repo
HTML_FILE = "/Users/marcelomansilla/proyectos/Workspaces/Radiaficion/ruedas/RUEDAS-MANEJA/rueda_en_la_cueva.html"  # Reemplaza con el nombre de tu archivo

def run_command(command):
    """Ejecuta un comando en la terminal y devuelve el resultado."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error ejecutando: {command}")
        print(result.stderr)
    return result.stdout.strip()

def update_github():
    os.chdir(REPO_PATH)

    # Verificar si hay cambios en el archivo HTML
    status = run_command(f"git status --porcelain {HTML_FILE}")

    if status:
        print("📌 Se detectaron cambios en el archivo HTML. Subiendo a GitHub...")
        
        # Agregar, confirmar y subir cambios
        run_command(f"git add {HTML_FILE}")
        run_command('git commit -m "Actualización automática del archivo HTML"')
        run_command("git push origin main")
        print("✅ Archivo actualizado en GitHub.")
    else:
        print("⏳ No hay cambios en el archivo. No se sube nada.")

# Ejecutar el script
update_github()
