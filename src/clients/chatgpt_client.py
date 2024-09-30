'''
Created on 19 jul 2024

Referencias:
 - https://ollama.com/
 - https://python.langchain.com/docs/integrations/chat/ollama/

@author: chispas
'''

from langchain_openai import ChatOpenAI
import getpass

##########################################################################################
import os
import traceback
# Obtener el nombre del script actual
nombre_script = os.path.basename(__file__)
# Mostrar el nombre del script
print(f"El nombre del script que se está ejecutando es: {nombre_script}")
##########################################################################################

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

# Inicializar el modelo de lenguaje
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)


def run():
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
    run()
