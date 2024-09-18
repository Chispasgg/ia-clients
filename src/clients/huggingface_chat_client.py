'../../conf/huggingface''''
Created on 19 jul 2024

Referencias:
 - https://huggingface.co
 - https://python.langchain.com/docs/integrations/chat/huggingface/

@author: chispas
'''

##########################################################################################
import os
import traceback
# Obtener el nombre del script actual
nombre_script = os.path.basename(__file__)
# Mostrar el nombre del script
print(f"El nombre del script que se está ejecutando es: {nombre_script}")
##########################################################################################

import getpass
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

path_hf_config_folder = '../conf'

def run():
    
    if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
        os.makedirs(path_hf_config_folder, exist_ok=True)
        path_hf_config_file = f"{path_hf_config_folder}/huggingface"
        if not os.path.isfile(path_hf_config_file):
            hf_token = getpass.getpass("Cual es tu token de huggingface? ")
        else:
            # Abrir el archivo en modo lectura
            with open(path_hf_config_file, 'r') as file:
                hf_token = file.read().strip()
    
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token
    
    hfe = HuggingFaceEndpoint(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        # repo_id="microsoft/Phi-3-mini-4k-instruct",
        # repo_id="mistralai/Mistral-7B-Instruct-v0.2",
        task="text-generation",
        max_new_tokens=1024,
        do_sample=False,
        repetition_penalty=1.03,
    )
    
    llm = ChatHuggingFace(llm=hfe, verbose=True)
    
    input_text = "Que te gustaría preguntar? Si quieres salir, escribe exit\n"
    prompt_del_sistema = ("system",
                          "You are a helpful assistant that helps user to achieve their goals")

    messages = [prompt_del_sistema]
    try:
        print("Soy un asistente para ayudarte.")
        pregunta = input(input_text)
        while pregunta != 'exit':
            messages.append(("human", pregunta))
            ai_msg = llm.invoke(messages)
            messages.append(("system", ai_msg.content))
            print(ai_msg.content)
            print("----------------------------------------------")
            pregunta = input(input_text)

    except:
        traceback.print_exc()

    print("========================================")
    print("Terminado")


if __name__ == "__main__":
    path_hf_config_folder = '../../conf'
    run()
    
