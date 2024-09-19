from flask import Flask, request, abort
import subprocess
import os

app = Flask(__name__)

# Configura la ruta de tu repositorio
REPO_DIR = '/path/to/your/repo'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # Verifica el contenido del payload si es necesario
        data = request.json

        # Cambia al directorio del repositorio
        os.chdir(REPO_DIR)
        
        # Actualiza el repositorio
        try:
            subprocess.check_call(['git', 'pull'])
            print("Repositorio actualizado.")
            
            # Ejecuta tu script o reinicia el programa
            subprocess.check_call(['python3', 'your_script.py'])
            print("Programa reiniciado.")
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el comando: {e}")

        return '', 200
    else:
        abort(400)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
