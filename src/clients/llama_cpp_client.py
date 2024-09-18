'''
Created on 19 jul 2024

Referencias:
 - https://ollama.com/
 - https://python.langchain.com/docs/integrations/chat/ollama/

@author: chispas
'''

import requests
import traceback

# Configuración básica
BASE_URL = "http://localhost:PORT/v1"
HEADERS = {"Authorization": "Bearer no-key", "Content-Type": "application/json"}

modelos_disponibles = {
    'Meta-Llama-3-8B-Instruct.Q4_K_S.gguf':'8081',
    'mistral-7b-instruct-v0.2.Q4_K_M.gguf':'8082',
    'gpt4all-falcon-newbpe-q4_0.gguf':'8083'
    }
                   

modelo_utilizar = modelos_disponibles[list(modelos_disponibles.keys())[0]]


# 1. POST /v1/chat/completions - Completa una conversación
def chat_completion(model, messages=None):
    """
    Este endpoint genera una respuesta de chat según los mensajes dados.
    Puedes personalizar el modelo y los mensajes de entrada.
    """
    if messages is None:
        messages = [
            {"role": "system", "content": "You are a helpful AI."},
            {"role": "user", "content": "¿Cuál es la capital de Francia?"}
        ]
    BASE_URL_tmp = BASE_URL.replace(":PORT/", f":{modelos_disponibles[model]}/")
    url = f"{BASE_URL_tmp}/chat/completions"
    data = {
        "model": model,
        "messages": messages
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    
    result = {}
    
    try:
        result = response.json()
    except:
        traceback.print_exc()  
    
    return result


# 2. POST /v1/embeddings - Obtener embeddings
def get_embeddings(model, input_text):
    """
    Este endpoint genera embeddings de texto a partir de la entrada dada.
    Utilizado para tareas de similaridad semántica.
    """
    url = f"{BASE_URL}/embeddings"
    data = {
        "input": input_text,
        "model": model,
        "encoding_format": "float"
    }
    
    response = requests.post(url, headers=HEADERS, json=data)
    result = {}
    
    try:
        result = response.json()
    except:
        traceback.print_exc()  
    
    return result


# 3. GET /slots - Obtener estado de los slots de procesamiento
def get_slots():
    """
    Este endpoint devuelve el estado actual de los slots de procesamiento.
    Se puede utilizar para monitorear el uso y disponibilidad de recursos.
    """
    url = f"{BASE_URL}/slots"
    response = requests.get(url, headers=HEADERS)
    result = {}
    
    try:
        result = response.json()
    except:
        traceback.print_exc()  
    
    return result


# 4. POST /slots/{id_slot}?action=save - Guardar caché de prompts
def save_slot(id_slot, filename):
    """
    Este endpoint guarda la caché de prompts de un slot específico en un archivo.
    """
    url = f"{BASE_URL}/slots/{id_slot}?action=save"
    data = {"filename": filename}
    
    response = requests.post(url, headers=HEADERS, json=data)
    result = {}
    
    try:
        result = response.json()
    except:
        traceback.print_exc()  
    
    return result


# 5. POST /slots/{id_slot}?action=restore - Restaurar caché de prompts
def restore_slot(id_slot, filename):
    """
    Este endpoint restaura la caché de prompts desde un archivo guardado.
    """
    url = f"{BASE_URL}/slots/{id_slot}?action=restore"
    data = {"filename": filename}
    
    response = requests.post(url, headers=HEADERS, json=data)
    result = {}
    
    try:
        result = response.json()
    except:
        traceback.print_exc()  
    
    return result


# 6. GET /metrics - Obtener métricas del servidor
def get_metrics():
    """
    Este endpoint devuelve métricas de rendimiento compatibles con Prometheus.
    Útil para monitorear el uso del servidor.
    """
    url = f"{BASE_URL}/metrics"
    response = requests.get(url, headers=HEADERS)
    
    result = None
    
    try:
        result = response.text
    except:
        traceback.print_exc()  
    
    return result


# Ejemplo de uso de los endpoints
def run():
    print("INICIO")
    
    for m in modelos_disponibles.keys():
        print(f" - Modelo: {m}")
    
    modelo_utilizar = input("Elige un modelo\n")
    
    input_text = "Que te gustaría preguntar? Si quieres salir, escribe exit\n"
    
    prompt_del_sistema = {"role": "system",
                          "content": "You are a helpful assistant that helps user to achieve their goals"}
    
    messages = [prompt_del_sistema]
    
    try:
        print("Soy un asistente para ayudarte.")
        pregunta = input(input_text)
        while pregunta != 'exit':
            # Prueba de completación de chat
            
            messages.append({"role": "user", "content": pregunta})
            response = chat_completion(modelo_utilizar, messages=messages)
    
            if response:
                print(f" Modelo usado: {response['model']}")
                print(f" Objetivo:     {response['object']}")
                print(f" Consumos:     {response['usage']}")
                for x in response['choices']:
                    print(f"    Respuesta con el rol de {x['message']['role']}: {x['message']['content']}")
                    messages.append({"role": "system", "content": x['message']['content']})
                
            else:
                print(" Sin respuesta")
            
            print("----------------------------------------------")
            pregunta = input(input_text)
        
    except:
        traceback.print_exc()
    
    print("========================================")
    print("Terminado")
    
    print("FIN")

    
if __name__ == "__main__":
    run()
