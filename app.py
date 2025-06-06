import os
import dotenv
from google import genai
import json
import re
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_client import api_client
from CoffeMaster import data_splitter, interpretador
dotenv.load_dotenv()
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings


GEMINI_API_KEY =  os.environ.get("CHAVE_GOOGLE")
client = genai.Client(api_key=GEMINI_API_KEY)
chat = client.chats.create(model="gemini-2.0-flash")

with open("Bot_Gerador_de_Personagens\data\Instrucoes.md", "r", encoding="utf-8") as f:
    instrucoes = f.read()




def extrair_json_de_markdown(texto_ia):
    match = re.search(r"```json\s*(\{.*?\})\s*```", texto_ia, re.DOTALL)
    if match:
        json_str = match.group(1)
        return json.loads(json_str)
    else:
         raise ValueError("JSON não encontrado na resposta da IA.")
    



def criarPersonagem(descricao):
    pergunta = interpretador.fazer_pergunta(f"o jogador quer criar um personagem com a seguinte descrição {descricao}")
    dados = data_splitter.fazer_busca(pergunta)
    dados_text = "\n\n".join([doc.page_content for doc in dados])
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[dados_text, instrucoes, descricao, "Com base nos dados enviados, leia as instruções e o livro do jogador e gere um personagem para o usuário"]
    )
    print(extrair_json_de_markdown(response.text))
    return extrair_json_de_markdown(response.text)
     
    
    


  

def alterarFicha(descricao, personagemNome, campanhaNome):
            personagem = api_client.buscarPersonagem(campanhaNome, personagemNome)
            response = chat.send_message(f"Você é um bot gerador de personagens para rpg, o usuário quer fazer a seguinte alteração {descricao}, no seguinte personagem {personagem}. leia os arquivos {[ instrucoes]} e faça as alterações desejadas" )
            print(extrair_json_de_markdown(response.text))
            api_client.atualizarPersonagem(campanhaNome, extrair_json_de_markdown(response.text))

