'''
Created on 16 sept 2024

@author: chispas
'''
from clients import ollama_client, llama_cpp_client, huggingface_chat_client

if __name__ == '__main__':
    print("INICIO")
    
    print("Sistema de ejemplos de clientes de IA")
    
    print("Agente llama.cpp")
    llama_cpp_client.run()
    
    print("Agente Huggingface")
    huggingface_chat_client.run()
    
    print("Agente Ollama")
    ollama_client.run()
    
    print("FIN")
