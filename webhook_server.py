from flask import Flask, request, abort
import subprocess
import os
import hmac
import hashlib
from webhookconfig import *

app = Flask(__name__)


def verify_signature(request):
    """
    Verifica la firma del webhook usando la clave secreta.
    """
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        return False

    # Calcula la firma esperada
    digest = hmac.new(SECRET, request.data, hashlib.sha256).hexdigest()
    expected_signature = f'sha256={digest}'

    return hmac.compare_digest(expected_signature, signature)

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Maneja las solicitudes POST del webhook.
    """
    # Verifica la firma del webhook
    if USE_SECRET and not verify_signature(request):
        abort(400, 'Invalid signature')

    # Verifica que el repositorio en el payload coincide con el esperado
    data = request.json
    # repository_name = data.get('repository', {}).get('name')
    # if repository_name != EXPECTED_REPO_NAME:
    #     abort(400, 'Not the expected repository')

    # Cambia al directorio del repositorio
    
    # Actualiza el repositorio
    try:
        os.chdir(REPO_DIR)
        
        subprocess.check_call(["git", "pull"])
        print("Repositorio actualizado.")
        
        # Ejecuta tu script o reinicia el programa
        subprocess.check_call(RESTART_CALL)
        print("Programa reiniciado.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")

    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
